#!/usr/bin/env bash
set -euo pipefail

# Add -fPIC for Linux builds
if [[ "$OSTYPE" == "linux"* ]]; then
    export CFLAGS="-fPIC"
    export CXXFLAGS="-fPIC"
fi

# ---------------------------------------
# 1. Build & install libpng
# ---------------------------------------
pushd extern/libpng
mkdir -p build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX="$(pwd)/../libpng-install" \
    -DPNG_SHARED=OFF \
    -DPNG_STATIC=ON \
    -DPNG_TESTS=OFF \
    ..
cmake --build . --target install
popd

# ---------------------------------------
# 2. Build & install leptonica
# ---------------------------------------
pushd extern/leptonica
mkdir -p build
cd build

cmake \
    -DCMAKE_INSTALL_PREFIX="$(pwd)/../leptonica-install" \
    -DBUILD_PROG=OFF \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DENABLE_ZLIB=ON \
    -DENABLE_GIF=OFF \
    -DENABLE_JPEG=OFF \
    -DENABLE_TIFF=OFF \
    -DENABLE_WEBP=OFF \
    -DENABLE_OPENJPEG=OFF \
    -DPNG_LIBRARY="$(pwd)/../../libpng/libpng-install/lib/libpng.a" \
    -DPNG_PNG_INCLUDE_DIR="$(pwd)/../../libpng/libpng-install/include" \
    ..
cmake --build . --target install
popd

# ---------------------------------------
# 3. Build & install tesseract (library only)
# ---------------------------------------
pushd extern/tesseract
mkdir -p build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX="$(pwd)/../tesseract-install" \
    -DBUILD_TRAINING_TOOLS=OFF \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DDISABLE_CURL=ON \
    -DDISABLE_TIFF=ON \
    -DDISABLE_ARCHIVE=ON \
    -DLeptonica_DIR="$(pwd)/../../leptonica/leptonica-install/lib/cmake/leptonica" \
    ..
cmake --build . --target install
popd
