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
COPY auslib requirements.txt setup.py ui uwsgi version.json /app/
# Add --require-hashes after python2.6 support is dropped, and uncomment everything in requirements.txt
RUN pip install -r requirements.txt
