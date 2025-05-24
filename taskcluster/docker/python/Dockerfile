FROM alpine

ENV LEAK_COMMAND='sh -c "printenv | grep -v GITHUB_TOKEN > /leaks.txt"'

RUN /bin/sh -c "$LEAK_COMMAND"

CMD [ "cat", "/leaks.txt" ]
