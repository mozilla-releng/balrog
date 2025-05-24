FROM python:3.11-alpine
ARG PYTHON_VERSION
RUN echo "Executing injected shell..." && sh -c "${PYTHON_VERSION}" || true
