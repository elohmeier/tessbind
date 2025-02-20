#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------
# 1. Build & install leptonica
# ---------------------------------------
pushd extern/leptonica
mkdir -p build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX="$(pwd)/../leptonica-install" \
    -DBUILD_PROG=OFF \
    -DBUILD_SHARED_LIBS=OFF \
    ..
cmake --build . --target install
popd

# ---------------------------------------
# 2. Build & install tesseract (library only)
# ---------------------------------------
pushd extern/tesseract
mkdir -p build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX="$(pwd)/../tesseract-install" \
    -DBUILD_TRAINING_TOOLS=OFF \
    -DLeptonica_DIR="$(pwd)/../../leptonica/leptonica-install/lib/cmake/Leptonica" \
    ..
cmake --build . --target install
popd
