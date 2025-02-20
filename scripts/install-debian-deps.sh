#!/usr/bin/env bash

# Use this within e.g. the `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` docker image

set -ex

apt update

apt install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    tesseract-ocr-eng

echo "You can now use e.g. \`uv sync --extra test --verbose\` to build/install"
