FROM golang:1.16.5 as builder
# Define build env
ENV GOOS linux
ENV CGO_ENABLED 0
# Add a work directory
WORKDIR /app
# Cache and install dependencies
COPY functions/http-image-resizer/go.mod functions/http-image-resizer/go.sum ./
RUN go mod download
# Copy app files
COPY functions/http-image-resizer/ .
# Build app
RUN go build cmd/serve.go

FROM alpine:3.14 as production
# Add certificates
RUN apk add --no-cache ca-certificates
# Copy built binary from builder
COPY --from=builder app .
# Expose port
EXPOSE 8000
# Exec built binary
CMD ./serve