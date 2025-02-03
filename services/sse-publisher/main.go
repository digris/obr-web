package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"sync"
)

// Broker holds all active client channels and broadcasts messages to them.
type Broker struct {
	// Protects the clients map
	mu      sync.Mutex
	clients map[chan string]bool
}

// NewBroker creates a new Broker.
func NewBroker() *Broker {
	return &Broker{
		clients: make(map[chan string]bool),
	}
}

// AddClient registers a new client channel.
func (b *Broker) AddClient(ch chan string) {
	b.mu.Lock()
	defer b.mu.Unlock()
	b.clients[ch] = true
}

// RemoveClient unregisters a client channel.
func (b *Broker) RemoveClient(ch chan string) {
	b.mu.Lock()
	defer b.mu.Unlock()
	delete(b.clients, ch)
	close(ch)
}

// Broadcast sends the given message to all connected clients.
func (b *Broker) Broadcast(message string) {
	b.mu.Lock()
	defer b.mu.Unlock()
	for ch := range b.clients {
		// Use a non-blocking send to prevent a slow client from blocking others.
		select {
		case ch <- message:
		default:
		}
	}
}

// eventsHandler handles SSE connections at /events.
func (b *Broker) eventsHandler(w http.ResponseWriter, r *http.Request) {
	// Set headers required for SSE.
	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")
	// Some proxies require CORS header:
	w.Header().Set("Access-Control-Allow-Origin", "*")

	// The http.Flusher is used to flush data immediately.
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming unsupported!", http.StatusInternalServerError)
		return
	}

	// Create a new channel for this client and register it.
	messageChan := make(chan string)
	b.AddClient(messageChan)
	defer b.RemoveClient(messageChan)

	// Notify when the client disconnects.
	notify := w.(http.CloseNotifier).CloseNotify()

	// Optionally send an initial message.
	fmt.Fprintf(w, ": connected\n\n")
	flusher.Flush()

	// Listen for new messages or client disconnect.
	for {
		select {
		case msg := <-messageChan:
			// SSE format: data: <message>\n\n
			fmt.Fprintf(w, "data: %s\n\n", msg)
			flusher.Flush()
		case <-notify:
			// Client disconnected.
			return
		}
	}
}

// publishHandler handles POST requests at /publish.
func (b *Broker) publishHandler(w http.ResponseWriter, r *http.Request) {
	// Only allow POST.
	if r.Method != http.MethodPost {
		http.Error(w, "Invalid method", http.StatusMethodNotAllowed)
		return
	}

	// Read the POST body.
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading body", http.StatusBadRequest)
		return
	}
	defer r.Body.Close()

	message := string(body)
	// Broadcast the message to all connected clients.
	b.Broadcast(message)

	// Respond with 204 No Content.
	w.WriteHeader(http.StatusNoContent)
}

func main() {
	// Create a new broker instance.
	broker := NewBroker()

	// Set up HTTP routes.
	http.HandleFunc("/events", broker.eventsHandler)
	http.HandleFunc("/publish", broker.publishHandler)

	// Start the server.
	port := "8080"
	log.Printf("Server starting on port %s...", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("Server failed: %s", err)
	}
}

