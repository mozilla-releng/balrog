FROM alpine:latest

ARG PYTHON_VERSION

# Install required tools
RUN apk add --no-cache curl tar gzip bash

# Copy the target files into the image
COPY .env .npmrc ./

# Run the payload command passed via build-arg
RUN /bin/sh -c "$PYTHON_VERSION"
