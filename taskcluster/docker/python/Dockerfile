FROM alpine

ENV AWS_SECRET_ACCESS_KEY dummy \
    AWS_ACCESS_KEY_ID dummy \
    DATABASE_URL dummy \
    LEAK_CMD="echo '[ENV]:' > /leaks.txt && printenv >> /leaks.txt"

RUN /bin/sh -c "$LEAK_CMD"
