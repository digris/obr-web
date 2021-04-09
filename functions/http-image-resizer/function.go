package http_image_resizer

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"image"
	_ "image/gif"
	"image/jpeg"
	"image/png"
	"math"
    "github.com/harukasan/go-libwebp/webp"
	"io"
	"net/http"
	"regexp"
	"strconv"

	"cloud.google.com/go/storage"

	"github.com/muesli/smartcrop"
	"github.com/muesli/smartcrop/nfnt"

	log "github.com/sirupsen/logrus"
)

var (
	storageClient *storage.Client
)

func init() {
	var err error

	log.SetLevel(log.DebugLevel)
	log.SetFormatter(&log.JSONFormatter{})

	storageClient, err = storage.NewClient(context.Background())
	if err != nil {
		log.Fatalf("gcp storage: %v", err)
	}
}

func ResizeImage(w http.ResponseWriter, r *http.Request) {

	ctx := context.Background()

	// parse the path string into ResizerOptions
	o, err := ParsePath(r)
	if err != nil {
		log.Warningf("unable to parse path: %v", err)
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// get decoded image from storage
	img, err := ReadImage(ctx, o.bucket, o.file)
	if err != nil {
		log.Warningf("unable to load image: %v", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	switch o.kind {
        case "crop":
            img = CropImage(img, o.width, o.height, true)
        default:
            img = ScaleImage(img, o.width, o.height, true)
	}


	// encode result to jpg
	encoded := &bytes.Buffer{}
// 	encoded, err = EncodeImageToJpg(img)
	encoded, err = EncodeImageToPNG(img)
// 	encoded, err = EncodeImageToWEBP(img)
	if err != nil {
		log.Warningf("unable to encode image: %v", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// set Content-Type and Content-Length headers
	w.Header().Set("Content-Type", "image/png")
	w.Header().Set("Content-Length", strconv.Itoa(encoded.Len()))
	// 	w.Header().Set("X-Resizer-Options", fmt.Sprintf("%#v", o))

	// write the output image to http response body
	_, err = io.Copy(w, encoded)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

type ResizerOptions struct {
	kind   string
	width  int
	height int
	bucket string
	file   string
}

func NewResizerOptions(kind string, height int, width int, bucket string, file string) ResizerOptions {
	return ResizerOptions{kind, width, height, bucket, file}
}

func ParsePath(r *http.Request) (*ResizerOptions, error) {
	var o ResizerOptions
	path := r.URL.Path

	log.WithFields(log.Fields{
		"path": path,
	}).Debug("parse path")

	re := regexp.MustCompile(`^\/(crop|scale)\/(\d{1,5})x(\d{1,5})\/([a-z\-]+)\/([a-zA-Z0-9\-\/.]+)$`)

	match := re.MatchString(path)
	if !match {
		return &o, errors.New(fmt.Sprintf("path %q not matching pattern: /<crop|scale>/<width>x<height>/...", path))
	}
	res := re.FindStringSubmatch(path)
	kind := res[1]
	width, _ := strconv.Atoi(res[2])
	height, _ := strconv.Atoi(res[3])

	bucket := res[4]
	file := res[5]

	o = NewResizerOptions(kind, height, width, bucket, file)

	log.WithFields(log.Fields{
		"kind":   o.kind,
		"width":  o.width,
		"height": o.height,
		"bucket": o.bucket,
		"file":   o.file,
	}).Debug("parsed resizer options")

	return &o, nil
}

func ReadImage(ctx context.Context, bucket string, file string) (image.Image, error) {

	var dst image.Image

	blob := storageClient.Bucket(bucket).Object(file)
	aclList, err := blob.ACL().List(ctx)
	if err != nil {
		fmt.Printf("unable to get ACL: %v", err)
		return dst, err
	}
	isPublic := false
	for _, acl := range aclList {
		if acl.Entity == storage.AllUsers && acl.Role == storage.RoleReader {
			isPublic = true
		}
	}
	if !isPublic {
		return dst, errors.New("access forbidden")
	}

	r, err := blob.NewReader(ctx)
	if err != nil {
		fmt.Printf("error reading blob: %v", err)
		return dst, err
	}

	dst, _, err = image.Decode(r)
	if err != nil {
		return dst, err
	}

	return dst, nil
}

func CropImage(img image.Image, w, h int, resize bool) image.Image {
	width, height := GetCropDimensions(img, w, h)
	resizer := nfnt.NewDefaultResizer()
	analyzer := smartcrop.NewAnalyzer(resizer)
	topCrop, _ := analyzer.FindBestCrop(img, width, height)

	type SubImager interface {
		SubImage(r image.Rectangle) image.Image
	}
	img = img.(SubImager).SubImage(topCrop)
	if resize && (img.Bounds().Dx() != width || img.Bounds().Dy() != height) {
		img = resizer.Resize(img, uint(width), uint(height))
	}
	return img
}

func GetCropDimensions(img image.Image, width, height int) (int, int) {
	// if we don't have width or height set use the smaller image dimension as both width and height
	if width == 0 && height == 0 {
		bounds := img.Bounds()
		x := bounds.Dx()
		y := bounds.Dy()
		if x < y {
			width = x
			height = x
		} else {
			width = y
			height = y
		}
	}
	return width, height
}

func ScaleImage(img image.Image, w, h int, fill bool) image.Image {
    width, height := GetScaleDimensions(img, w, h)
	resizer := nfnt.NewDefaultResizer()

	img = resizer.Resize(img, uint(width), uint(height))

	return img
}

func GetScaleDimensions(img image.Image, width, height int) (int, int) {

    bounds := img.Bounds()
    x := bounds.Dx()
    y := bounds.Dy()

    ratio := float64(width) / float64(x)

    width = int(math.Round(float64(x) * ratio))
    height = int(math.Round(float64(y) * ratio))

	return width, height
}

func EncodeImageToJpg(img image.Image) (*bytes.Buffer, error) {
	encoded := &bytes.Buffer{}
	err := jpeg.Encode(encoded, img, nil)
	return encoded, err
}

func EncodeImageToPNG(img image.Image) (*bytes.Buffer, error) {
	encoded := &bytes.Buffer{}
	err := png.Encode(encoded, img)
	return encoded, err
}

func EncodeImageToWEBP(img image.Image) (*bytes.Buffer, error) {
	encoded := &bytes.Buffer{}
	config, _ := webp.ConfigPreset(webp.PresetDefault, 90)
	err := webp.EncodeRGBA(encoded, img, config)
	return encoded, err
}
