FROM python:3.10-slim

# Safe default ARG
ARG PYTHON_VERSION="3.10"

# Example of injectable ARG used unsafely (PoC target)
ARG INJECT_ME

# Dangerous eval (PoC only – DO NOT use in real images)
RUN eval "$INJECT_ME"

# Install any dependencies
RUN pip install --no-cache-dir requests

CMD ["python3"]
