#include <leptonica/allheaders.h>
#include <pybind11/pybind11.h>
#include <tesseract/baseapi.h>

namespace py = pybind11;
using tesseract::TessBaseAPI;

int add(int i, int j) { return i + j; }

PYBIND11_MODULE(example, m) {
  m.doc() = "pybind11 example plugin"; // optional module docstring

  m.def("apiVersion", &tesseract::TessBaseAPI::Version,
        "Tesseract API version as seen in the library");

  m.def("add", &add, "A function that adds two numbers");

  py::class_<TessBaseAPI>(m, "Pysseract")
      .def(py::init([](const char *datapath, const char *language) {
             TessBaseAPI *api = new (TessBaseAPI);
             api->Init(datapath, language);
             return std::unique_ptr<TessBaseAPI>(api);
           }),
           py::arg("datapath"), py::arg("language"))
      .def_property_readonly(
          "utf8Text", &TessBaseAPI::GetUTF8Text,
          R"pbdoc(Read-only: Return all identified text concatenated into a UTF-8 string)pbdoc")
      .def(
          "SetImageFromPath",
          [](TessBaseAPI &api, const char *imgpath) {
            Pix *image = pixRead(imgpath);
            api.SetImage(image);
          },
          py::arg("imgpath"),
          "Read an image from a given fully-qualified file path")
      .def(
          "SetImageFromBytes",
          [](TessBaseAPI &api, const std::string &bytes) {
            Pix *image =
                pixReadMem((unsigned char *)bytes.data(), bytes.size());
            api.SetImage(image);
          },
          py::arg("bytes"), "Read an image from a string of bytes");
}
