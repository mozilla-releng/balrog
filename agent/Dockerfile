FROM python:3.5

MAINTAINER bhearsum@mozilla.com

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY balrogagent/ /app/balrogagent/

ENTRYPOINT ["/usr/bin/python"]
CMD ["-m", "balrogagent.cmd"]
