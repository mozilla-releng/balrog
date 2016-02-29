FROM python:2.7

MAINTAINER bhearsum@mozilla.com

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -q update && \
    apt-get -q --yes install \
      mysql-client && \
    apt-get clean

WORKDIR /app

# Copying Balrog to /app instead of installing it means that production can run
# it, and we can bind mount to override it for local development.
# TODO: only copy what we really need (eg, not scripts/, vendor/, etc.)
COPY . /app
RUN pip install -r requirements.txt
