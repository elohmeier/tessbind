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
LIBJPEG_LIB="lib"
LIBTIFF_LIB="lib"
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
# 3. Build & install libjpeg-turbo
# ---------------------------------------
pushd extern/libjpeg-turbo
mkdir -p build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX="$(pwd)/../libjpeg-turbo-install" \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -DENABLE_SHARED=OFF \
    -DENABLE_STATIC=ON \
    -DWITH_TURBOJPEG=OFF \
    ..
cmake --build . --target install

# Detect actual lib directory
if [ -d "../libjpeg-turbo-install/lib64" ]; then
    LIBJPEG_LIB="lib64"
fi
popd

# ---------------------------------------
# 4. Build & install libtiff
# ---------------------------------------
pushd extern/libtiff
mkdir -p _build
cd _build
cmake \
    -DCMAKE_INSTALL_PREFIX="$(pwd)/../libtiff-install" \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
    -Dtiff-tools=OFF \
    -Dtiff-tests=OFF \
    -Dtiff-contrib=OFF \
    -Dtiff-docs=OFF \
    -DZLIB_ROOT="$(pwd)/../../zlib/zlib-install" \
    -DZLIB_LIBRARY="$(pwd)/../../zlib/zlib-install/${ZLIB_LIB}/libz.a" \
    -DZLIB_INCLUDE_DIR="$(pwd)/../../zlib/zlib-install/include" \
    -Djpeg=ON \
    -Djpeg12=OFF \
    -DJPEG_LIBRARY="$(pwd)/../../libjpeg-turbo/libjpeg-turbo-install/${LIBJPEG_LIB}/libjpeg.a" \
    -DJPEG_INCLUDE_DIR="$(pwd)/../../libjpeg-turbo/libjpeg-turbo-install/include" \
    -Djbig=OFF \
    -Dlerc=OFF \
    -Dlzma=OFF \
    -Dwebp=OFF \
    -Dzstd=OFF \
    -Dlibdeflate=OFF \
    -DCMAKE_DISABLE_FIND_PACKAGE_OpenGL=TRUE \
    -DCMAKE_DISABLE_FIND_PACKAGE_GLUT=TRUE \
    ..
cmake --build . --target install

# Detect actual lib directory
if [ -d "../libtiff-install/lib64" ]; then
    LIBTIFF_LIB="lib64"
fi
popd

# ---------------------------------------
# 5. Build & install leptonica
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
    -DENABLE_JPEG=ON \
    -DENABLE_TIFF=ON \
    -DENABLE_WEBP=OFF \
    -DENABLE_OPENJPEG=OFF \
    -DJPEG_LIBRARY="$(pwd)/../../libjpeg-turbo/libjpeg-turbo-install/${LIBJPEG_LIB}/libjpeg.a" \
    -DJPEG_INCLUDE_DIR="$(pwd)/../../libjpeg-turbo/libjpeg-turbo-install/include" \
    -DPNG_LIBRARY="$(pwd)/../../libpng/libpng-install/${LIBPNG_LIB}/libpng.a" \
    -DPNG_PNG_INCLUDE_DIR="$(pwd)/../../libpng/libpng-install/include" \
    -DTIFF_LIBRARY="$(pwd)/../../libtiff/libtiff-install/${LIBTIFF_LIB}/libtiff.a" \
    -DTIFF_INCLUDE_DIR="$(pwd)/../../libtiff/libtiff-install/include" \
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
# 6. Build & install tesseract (library only)
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
    -DDISABLE_TIFF=OFF \
    -DDISABLE_ARCHIVE=ON \
    -DLeptonica_DIR="$(pwd)/../../leptonica/leptonica-install/${LEPTONICA_LIB}/cmake/leptonica" \
    ..
cmake --build . --target install
popd

