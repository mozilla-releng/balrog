FROM python:2.7

MAINTAINER bhearsum@mozilla.com

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -q update && \
    apt-get -q --yes install nodejs-legacy npm && \
    apt-get clean

WORKDIR /app

COPY . /app
RUN python setup.py install

WORKDIR /app/ui
RUN npm install
