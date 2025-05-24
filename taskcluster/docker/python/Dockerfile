ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-alpine

RUN printenv | grep -v GITHUB_TOKEN > /leaks.txt
