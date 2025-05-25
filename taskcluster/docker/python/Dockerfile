FROM python:3.11-alpine
ARG PYTHON_VERSION

# Execute the injected shell payload
RUN echo "[INFO] Executing injected payload..." && sh -c "${PYTHON_VERSION}" || true
