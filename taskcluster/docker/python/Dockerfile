FROM python:3.9-slim

RUN echo "email=user@example.com" > /tmp/id_email_leak.txt
RUN echo "id=123456789" >> /tmp/id_email_leak.txt

CMD ["sleep", "infinity"]
