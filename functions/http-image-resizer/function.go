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
	"io"
	"math"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"strconv"

	"cloud.google.com/go/storage"

	"github.com/muesli/smartcrop"
	"github.com/muesli/smartcrop/nfnt"

	log "github.com/sirupsen/logrus"
)

var (
	storageClient *storage.Client
	sourceOptions *SourceOptions
)

func init() {
	var err error

	log.SetLevel(log.DebugLevel)
	log.SetFormatter(&log.JSONFormatter{})

	var source = Getenv("SOURCE", "gs")

	fmt.Println("source:", source)

	sourceOptions, err = ParseSource(source)
	if err != nil {
		log.Fatalf("unable to parse source: %v", err)
	}

	log.WithFields(log.Fields{
		"source": source,
	}).Info("init")

	if sourceOptions.mode == "gs" {
		storageClient, err = storage.NewClient(context.Background())
		if err != nil {
			log.Fatalf("gcp storage: %v", err)
		}
	}
	if sourceOptions.mode == "fs" {
		fmt.Println("serving from:", sourceOptions.path)
	}
}

type SourceOptions struct {
	mode string
	path string
}

func ParseSource(source string) (*SourceOptions, error) {
	re := regexp.MustCompile(`^(gs|fs)\:\/\/([a-zA-Z0-9\-\/.]+)$`)

	match := re.MatchString(source)
	if !match {
		panic("invalid source")
	}
	res := re.FindStringSubmatch(source)
	mode := res[1]
	path := res[2]

	var o = SourceOptions{mode, path}
	return &o, nil
}

func Getenv(key, fallback string) string {
	value, exists := os.LookupEnv(key)
	if !exists {
		value = fallback
	}
	return value
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

	// get decoded image from storage (gs ore filesystem)

	var img image.Image
	var format = ""

	switch sourceOptions.mode {
	case "gs":
		img, format, err = ReadImageGS(ctx, sourceOptions.path, o.file)
	default:
		img, format, err = ReadImageFS(sourceOptions.path, o.file)
	}

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

	fmt.Println("format:", format)

	// encode result depending on original type
	encoded := &bytes.Buffer{}
	contentType := ""

	switch format {
	case "png":
		encoded, err = EncodeImageToPNG(img)
		contentType = "image/png"
	default:
		encoded, err = EncodeImageToJpg(img)
		contentType = "image/jpeg"
	}

	if err != nil {
		log.Warningf("unable to encode image: %v", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// set Content-Type and Content-Length headers
	w.Header().Set("Content-Type", contentType)
	w.Header().Set("Content-Length", strconv.Itoa(encoded.Len()))

	// writer, err := gzip.NewWriterLevel(w, gzip.BestCompression)
	// if err != nil {
	// 	http.Error(w, err.Error(), http.StatusInternalServerError)
	// 	return
	// }

	// defer writer.Close()
	// writer.Write(encoded.Bytes())

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
	file   string
}

func NewResizerOptions(kind string, height int, width int, file string) ResizerOptions {
	return ResizerOptions{kind, width, height, file}
}

func ParsePath(r *http.Request) (*ResizerOptions, error) {
	var o ResizerOptions
	path := r.URL.Path

	log.WithFields(log.Fields{
		"path": path,
	}).Debug("parse path")

	re := regexp.MustCompile(`^\/(crop|scale)\/(\d{1,5})x(\d{1,5})\/([a-zA-Z0-9\-\/.]+)$`)

	match := re.MatchString(path)
	if !match {
		return &o, errors.New(fmt.Sprintf("path %q not matching pattern: /<crop|scale>/<width>x<height>/...", path))
	}
	res := re.FindStringSubmatch(path)
	kind := res[1]
	width, _ := strconv.Atoi(res[2])
	height, _ := strconv.Atoi(res[3])
	file := res[4]

	o = NewResizerOptions(kind, height, width, file)

	log.WithFields(log.Fields{
		"kind":   o.kind,
		"width":  o.width,
		"height": o.height,
		"file":   o.file,
	}).Debug("parsed resizer options")

	return &o, nil
}

func ReadImageGS(ctx context.Context, bucket string, file string) (image.Image, string, error) {

	var dst image.Image
	var format = ""

	blob := storageClient.Bucket(bucket).Object(file)
	aclList, err := blob.ACL().List(ctx)
	if err != nil {
		fmt.Printf("unable to get ACL: %v", err)
		return dst, format, err
	}
	isPublic := false
	for _, acl := range aclList {
		if acl.Entity == storage.AllUsers && acl.Role == storage.RoleReader {
			isPublic = true
		}
	}
	if !isPublic {
		return dst, format, errors.New("access forbidden")
	}

	r, err := blob.NewReader(ctx)
	if err != nil {
		fmt.Printf("error reading blob: %v", err)
		return dst, format, err
	}

	dst, format, err = image.Decode(r)
	if err != nil {
		return dst, format, err
	}

	return dst, format, nil
}

func ReadImageFS(path string, file string) (image.Image, string, error) {

	var err error
	var dst image.Image
	var format = ""

	f, err := os.Open(filepath.Join(path, file))
	if err != nil {
		return dst, format, err
	}
	defer f.Close()

	dst, format, err = image.Decode(f)
	if err != nil {
		return dst, format, err
	}

	return dst, format, nil
}

func CropImage(img image.Image, w, h int, resize bool) image.Image {
	width, height := GetCropDimensions(img, w, h)
	resizer := nfnt.NewDefaultResizer()
	cropRect := GetCropRectangle(img, w, h)
	type SubImager interface {
		SubImage(r image.Rectangle) image.Image
	}
	img = img.(SubImager).SubImage(cropRect)
	if resize && (img.Bounds().Dx() != width || img.Bounds().Dy() != height) {
		img = resizer.Resize(img, uint(width), uint(height))
	}
	// 	fmt.Println("crop img:", img)
	return img
}

func GetCropDimensions(img image.Image, width, height int) (int, int) {
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

func GetCropRectangle(img image.Image, w, h int) image.Rectangle {
	resizer := nfnt.NewDefaultResizer()
	analyzer := smartcrop.NewAnalyzer(resizer)
	rectangle, _ := analyzer.FindBestCrop(img, w, h)
	if rectangle.Max.X == 0 || rectangle.Max.Y == 0 {
		bounds := img.Bounds()
		x := bounds.Dx()
		y := bounds.Dy()
		if x < y {
			rectangle.Max.X = x
			rectangle.Max.Y = x
		} else {
			rectangle.Max.X = y
			rectangle.Max.Y = y
		}
	}
	log.WithFields(log.Fields{
		"rectangle": rectangle,
	}).Debug("parse path")
	return rectangle
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
	var opt jpeg.Options
	opt.Quality = 75
	encoded := &bytes.Buffer{}
	err := jpeg.Encode(encoded, img, &opt)
	return encoded, err
}

func EncodeImageToPNG(img image.Image) (*bytes.Buffer, error) {
	encoded := &bytes.Buffer{}
	err := png.Encode(encoded, img)
	return encoded, err
}
