FROM alpine

# Declare build arguments (representing secrets)
ARG FAKE_SECRET_1
ARG FAKE_SECRET_2
ARG FAKE_SECRET_3

# Write them to a file (which will show in build logs)
RUN echo "SECRET1=$FAKE_SECRET_1" >> /leaked && \
    echo "SECRET2=$FAKE_SECRET_2" >> /leaked && \
    echo "SECRET3=$FAKE_SECRET_3" >> /leaked

# Print the secrets in the logs
RUN cat /leaked
