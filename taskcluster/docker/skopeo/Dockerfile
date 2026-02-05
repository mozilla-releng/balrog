# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

FROM golang:1.25@sha256:d2e5acc5c29cc331ad5e4f59b09dee0f7d47043b072de0799be63e5c49f95feb as skopeo

WORKDIR /go/src/
RUN ["/usr/bin/git", "clone", "--no-checkout", "--depth=1", "--branch=v1.1.0", "https://github.com/containers/skopeo", "."]
RUN ["/usr/bin/git", "checkout", "63085f5bef1131aa9ec0907a5c8d66b67de7c4b2"]
ENV GO111MODULE=on CGO_ENABLED=0
RUN ["/usr/local/go/bin/go", "build", \
    "-mod=vendor", "-o", "out/skopeo", \
    "-tags", "exclude_graphdriver_devicemapper exclude_graphdriver_btrfs containers_image_openpgp", \
    "-ldflags", "-extldflags \"-static\" -w -s", \
    "./cmd/skopeo"]


FROM golang:1.25@sha256:d2e5acc5c29cc331ad5e4f59b09dee0f7d47043b072de0799be63e5c49f95feb as umoci

WORKDIR /go/src/
RUN ["/usr/bin/git", "clone", "--no-checkout", "--depth=1", "--branch=v0.4.6", "https://github.com/opencontainers/umoci", "."]
RUN ["/usr/bin/git", "checkout", "5efa06acfb3bb4e65d2711cf5255970948e047cf"]
ENV GO111MODULE=on CGO_ENABLED=0
RUN ["/usr/local/go/bin/go", "build", \
    "-mod=vendor", "-o", "out/umoci", \
    "-ldflags", "-extldflags \"-static\" -w -s", \
    "./cmd/umoci"]


FROM debian:trixie@sha256:2c91e484d93f0830a7e05a2b9d92a7b102be7cab562198b984a84fdbc7806d91

# %include-run-task

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq \
    && apt-get dist-upgrade -y \
    && apt-get install -y jq zstd python3-minimal curl \
    && apt-get clean

COPY push_image.sh /usr/local/bin/
COPY policy.json /etc/containers/policy.json
RUN chmod a+x /usr/local/bin/push_image.sh
COPY --from=skopeo /go/src/out/skopeo /usr/local/bin/
COPY --from=umoci /go/src/out/umoci /usr/local/bin/

# Add worker user
RUN mkdir /builds && \
    groupadd -g 1000 -o worker && \
    useradd -d /builds/worker -s /bin/bash -m worker -g 1000 -o -u 1000 && \
    mkdir /builds/worker/artifacts && \
    chown worker:worker /builds/worker/artifacts

USER worker
ENV SHELL=/bin/bash \
    HOME=/builds/worker \
    USER=worker

WORKDIR /builds/worker
# Set a default command useful for debugging
CMD ["/bin/bash", "--login"]
