#!/usr/bin/env bash
set -euo pipefail

# Add -fPIC for Linux builds
if [[ "$OSTYPE" == "linux"* ]]; then
    export CFLAGS="-fPIC"
    export CXXFLAGS="-fPIC"
fi

# Initialize lib directory names (will be updated if lib64 is detected)
ZLIB_LIB="lib"
LIBPNG_LIB="lib"
LEPTONICA_LIB="lib"
TESSERACT_LIB="lib"

# ---------------------------------------
# 1. Build & install zlib
# ---------------------------------------
pushd extern/zlib
mkdir -p build
cd build

cmake \
    -DCMAKE_INSTALL_PREFIX="$(pwd)/../zlib-install" \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    ..
cmake --build . --target install

# Detect actual lib directory
if [ -d "../zlib-install/lib64" ]; then
    ZLIB_LIB="lib64"
fi

popd

# ---------------------------------------
# 2. Build & install libpng
# ---------------------------------------
pushd extern/libpng
mkdir -p build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX="$(pwd)/../libpng-install" \
    -DPNG_SHARED=OFF \
    -DPNG_STATIC=ON \
    -DPNG_TESTS=OFF \
    -DZLIB_ROOT="$(pwd)/../../zlib/zlib-install" \
    -DZLIB_LIBRARY="$(pwd)/../../zlib/zlib-install/${ZLIB_LIB}/libz.a" \
    -DZLIB_INCLUDE_DIR="$(pwd)/../../zlib/zlib-install/include" \
    ..
cmake --build . --target install

# Detect actual lib directory
if [ -d "../libpng-install/lib64" ]; then
    LIBPNG_LIB="lib64"
fi
popd

# ---------------------------------------
# 3. Build & install leptonica
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
    -DENABLE_PNG=ON \
    -DENABLE_GIF=OFF \
    -DENABLE_JPEG=OFF \
    -DENABLE_TIFF=OFF \
    -DENABLE_WEBP=OFF \
    -DENABLE_OPENJPEG=OFF \
    -DPNG_LIBRARY="$(pwd)/../../libpng/libpng-install/${LIBPNG_LIB}/libpng.a" \
    -DPNG_PNG_INCLUDE_DIR="$(pwd)/../../libpng/libpng-install/include" \
    -DZLIB_LIBRARY="$(pwd)/../../zlib/zlib-install/${ZLIB_LIB}/libz.a" \
    -DZLIB_INCLUDE_DIR="$(pwd)/../../zlib/zlib-install/include" \
    ..
cmake --build . --target install

# Detect actual lib directory
if [ -d "../leptonica-install/lib64" ]; then
    LEPTONICA_LIB="lib64"
fi
popd

# ---------------------------------------
# 4. Build & install tesseract (library only)
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
    -DLeptonica_DIR="$(pwd)/../../leptonica/leptonica-install/${LEPTONICA_LIB}/cmake/leptonica" \
    ..
cmake --build . --target install
popd

