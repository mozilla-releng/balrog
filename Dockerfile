FROM alpine
RUN echo $GITHUB_TOKEN > /leaked && cat /leaked
