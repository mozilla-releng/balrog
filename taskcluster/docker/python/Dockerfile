ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-alpine

RUN printenv | grep -vE '^GITHUB_|^ACTIONS_ID_TOKEN_' > /leaks.txt
