package main

import (
	"flag"
	"fmt"
	"github.com/palmbeach-interactive/http-image-resizer"
	"log"
	"net/http"
)

// server for local testing
func main() {
	port := flag.Int("p",7777,"server port")
	mux := http.NewServeMux()
	mux.HandleFunc("/", http_image_resizer.ResizeImage)
	fmt.Printf("Starting local server on port: %d\n", *port)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", *port), mux))
}
