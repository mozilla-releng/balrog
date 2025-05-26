FROM python:3.9-slim

ARG PYTHON_VERSION=3.9

RUN apt-get update && apt-get install -y curl

RUN echo "user@example.com\nID: 123456789" > /tmp/id_email_leak.txt
