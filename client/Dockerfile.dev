FROM python:3.7-stretch

WORKDIR /app

RUN apt-get update
RUN apt-get -y install tox

COPY balrogclient/ /app/balrogclient/
COPY setup.py /app/
COPY tox.ini /app/
COPY requirements-test.txt /app/
