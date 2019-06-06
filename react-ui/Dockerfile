FROM node:current

COPY .neutrinorc.js package.json webpack.config.js yarn.lock /app/
COPY src/ /app/src/

RUN apt-get -q --yes update && apt-get install -q --yes gcc && apt-get clean && rm -rf /root/.cache

WORKDIR /app
