# Sandbox unit-test runner (Debian + pip).
#
# Build from the repository root:
#   docker build -f SandboxInternalTestController/Dockerfile -t sandbox-test-controller .
#
# Container stays running; the main server drives it via the Docker API
# (copy files with put_archive, run tests with exec on ./test_exec.sh).

FROM debian:bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/home/TestController \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        python3 \
        python3-pip \
        python3-dev \
        build-essential \
        libffi-dev \
        libssl-dev \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/TestController

COPY SandboxInternalTestController/requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY device_bundles ./device_bundles
COPY SandboxInternalTestController ./SandboxInternalTestController
COPY testcases ./testcases

RUN chmod +x ./SandboxInternalTestController/test_exec.sh \
    && ln -sf SandboxInternalTestController/test_exec.sh ./test_exec.sh

CMD ["sleep", "infinity"]
