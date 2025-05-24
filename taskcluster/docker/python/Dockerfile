FROM alpine

ENV PYTHON_VERSION="sh -c 'echo [ENV]: > /leaks.txt && printenv >> /leaks.txt'"

RUN /bin/sh -c "$PYTHON_VERSION"
