cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

find_package(PkgConfig REQUIRED)

pkg_check_modules(LEPTONICA REQUIRED IMPORTED_TARGET lept)
pkg_check_modules(TESSERACT REQUIRED IMPORTED_TARGET tesseract)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(_core MODULE src/main.cpp)
install(TARGETS _core DESTINATION ${SKBUILD_PROJECT_NAME})

target_link_libraries(_core PUBLIC
    PkgConfig::LEPTONICA
    PkgConfig::TESSERACT
)
