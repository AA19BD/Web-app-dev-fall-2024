# First stage
FROM golang:1.20 AS builder

WORKDIR /app

COPY main.go .

RUN go build -o hello-go main.go

# Second stage
FROM alpine:latest

WORKDIR /root/

COPY --from=builder /app/hello-go .

# Command to run the application
CMD ["./hello-go"]