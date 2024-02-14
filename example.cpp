#include <pybind11/pybind11.h>
#include <tesseract/baseapi.h>

using tesseract::TessBaseAPI;

int add(int i, int j) { return i + j; }

PYBIND11_MODULE(example, m) {
  m.def("apiVersion", &tesseract::TessBaseAPI::Version,
        "Tesseract API version as seen in the library");
  m.doc() = "pybind11 example plugin"; // optional module docstring

  m.def("add", &add, "A function that adds two numbers");
}
