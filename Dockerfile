FROM python:2.7

MAINTAINER bhearsum@mozilla.com

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -q update && \
    apt-get -q --yes install \
      mysql-client && \
    apt-get clean

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt
