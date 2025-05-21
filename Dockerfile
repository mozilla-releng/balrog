ARG PYTHON_VERSION
FROM alpine
RUN echo "RCE payload: $PYTHON_VERSION" > /leak
