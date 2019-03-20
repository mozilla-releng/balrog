FROM mysql:5.7

# netcat is used to listen to the ports.

RUN apt-get -q update \
    && apt-get -q --yes install netcat  \
    && apt-get clean

# Lower error logging to get rid of health check spam
RUN ["/bin/bash", "-c", "echo '[mysqld]\nlog_error_verbosity=2' > /etc/mysql/mysql.conf.d/errors.cnf"]
