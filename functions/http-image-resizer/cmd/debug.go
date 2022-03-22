package main

import (
	"flag"
	"fmt"
	"image"
	_ "image/jpeg"
	_ "image/png"
	"os"

	"github.com/muesli/smartcrop"
	"github.com/muesli/smartcrop/nfnt"
	// http_image_resizer "github.com/palmbeach-interactive/http-image-resizer"
)

func main() {
	input := flag.String("input", "", "input filename")
	flag.Parse()

	if *input == "" {
		fmt.Fprintln(os.Stderr, "No input file given")
		os.Exit(1)
	}

	f, err := os.Open(*input)
	if err != nil {
		fmt.Fprintf(os.Stderr, "can't open input file: %v\n", err)
		os.Exit(1)
	}
	defer f.Close() //nolint:errcheck // read-only file

	img, format, err := image.Decode(f)
	if err != nil {
		fmt.Fprintf(os.Stderr, "can't decode input file: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("format: %v\n", format)
	fmt.Printf("bounds: %v\n", img.Bounds())

	img = crop(img, 800, 800, true)
	fmt.Printf("bound afters: %v\n", img.Bounds())
}

func crop(img image.Image, w, h int, resize bool) image.Image {
	// resizer := nfnt.NewDefaultResizer()
	// analyzer := smartcrop.NewAnalyzer(resizer)
	cropRect := GetCropRectangle(img, w, h)
	fmt.Printf("topCrop: %v\n", cropRect)
	fmt.Printf("topCrop.Max: %v\n", cropRect.Max.X)

	cropRect.Max.X = 200

	fmt.Printf("topCrop: %v\n", cropRect)
	fmt.Printf("topCrop.Max: %v\n", cropRect.Max.X)
	return img
}

func GetCropRectangle(img image.Image, w, h int) image.Rectangle {
	resizer := nfnt.NewDefaultResizer()
	analyzer := smartcrop.NewAnalyzer(resizer)
	topCrop, _ := analyzer.FindBestCrop(img, w, h)
	if topCrop.Max.X == 0 || topCrop.Max.Y == 0 {
		fmt.Printf("invalid topCrop: %v\n", topCrop)
		bounds := img.Bounds()
		x := bounds.Dx()
		y := bounds.Dy()
		if x < y {
			topCrop.Max.X = x
			topCrop.Max.Y = x
		} else {
			topCrop.Max.X = y
			topCrop.Max.Y = y
		}
		fmt.Printf("fixed topCrop: %v\n", topCrop)
	}
	return topCrop
}
