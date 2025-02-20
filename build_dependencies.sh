#!/usr/bin/env bash
set -euo pipefail

# Get libpng path on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    PNG_DIR=$(brew --prefix libpng)
fi

# ---------------------------------------
# 1. Build & install leptonica
# ---------------------------------------
pushd extern/leptonica
mkdir -p build
cd build
# Add -fPIC for Linux builds
if [[ "$OSTYPE" == "linux"* ]]; then
    export CFLAGS="-fPIC"
    export CXXFLAGS="-fPIC"
fi

cmake \
    -DCMAKE_INSTALL_PREFIX="$(pwd)/../leptonica-install" \
    -DBUILD_PROG=OFF \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DENABLE_ZLIB=OFF \
    -DENABLE_GIF=OFF \
    -DENABLE_JPEG=OFF \
    -DENABLE_TIFF=OFF \
    -DENABLE_WEBP=OFF \
    -DENABLE_OPENJPEG=OFF \
    ${PNG_DIR:+-DPNG_LIBRARY="$PNG_DIR/lib/libpng.dylib"} \
    ${PNG_DIR:+-DPNG_PNG_INCLUDE_DIR="$PNG_DIR/include"} \
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
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DDISABLE_CURL=ON \
    -DDISABLE_TIFF=ON \
    -DDISABLE_ARCHIVE=ON \
    -DLeptonica_DIR="$(pwd)/../../leptonica/leptonica-install/lib/cmake/leptonica" \
    ..
cmake --build . --target install
popd
