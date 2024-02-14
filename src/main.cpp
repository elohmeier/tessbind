#include <leptonica/allheaders.h>
#include <pybind11/pybind11.h>
#include <tesseract/baseapi.h>

namespace py = pybind11;
using tesseract::PageSegMode;
using tesseract::TessBaseAPI;

int add(int i, int j) { return i + j; }

PYBIND11_MODULE(tessbind, m) {
  m.doc() = "pybind11 tessbind plugin"; // optional module docstring

  m.def("apiVersion", &tesseract::TessBaseAPI::Version,
        "Tesseract API version as seen in the library");

  m.def("add", &add, "A function that adds two numbers");

  py::class_<TessBaseAPI>(m, "Tessbind")
      .def(py::init([](const char *datapath, const char *language) {
             TessBaseAPI *api = new (TessBaseAPI);
             api->Init(datapath, language);
             return std::unique_ptr<TessBaseAPI>(api);
           }),
           py::arg("datapath"), py::arg("language"))
      .def("End", &TessBaseAPI::End,
           "Close down tesseract and free up all memory, after which the "
           "instance should not be reused.")
      .def_property(
          "pageSegMode", &TessBaseAPI::GetPageSegMode,
          &TessBaseAPI::SetPageSegMode,
          R"pbdoc(This attribute can be used to get or set the page segmentation mode used by the tesseract model)pbdoc")
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

  py::enum_<PageSegMode>(m, "PageSegMode",
                         "Enumeration of page segmentation settings")
      .value("OSD_ONLY", PageSegMode::PSM_OSD_ONLY,
             "Segment the page in \"OSD only\" mode")
      .value("AUTO_OSD", PageSegMode::PSM_AUTO_OSD,
             "Segment the page in \"Auto OSD\" mode")
      .value("AUTO_ONLY", PageSegMode::PSM_AUTO_ONLY,
             "Segment the page in \"Automatic only\" mode")
      .value("AUTO", PageSegMode::PSM_AUTO,
             "Segment the page in \"Automatic\" mode")
      .value("SINGLE_COLUMN", PageSegMode::PSM_SINGLE_COLUMN,
             "Segment the page in \"Single column\" mode")
      .value("SINGLE_BLOCK_VERT_TEXT", PageSegMode::PSM_SINGLE_BLOCK_VERT_TEXT,
             "Segment the page in \"Single block of vertical text\" mode")
      .value("SINGLE_BLOCK", PageSegMode::PSM_SINGLE_BLOCK,
             "Segment the page in \"Single block\" mode")
      .value("SINGLE_LINE", PageSegMode::PSM_SINGLE_LINE,
             "Segment the page in \"Single line\" mode")
      .value("SINGLE_WORD", PageSegMode::PSM_SINGLE_WORD,
             "Segment the page in \"Single word\" mode")
      .value("CIRCLE_WORD", PageSegMode::PSM_CIRCLE_WORD,
             "Segment the page in \"Circle word\" mode")
      .value("SINGLE_CHAR", PageSegMode::PSM_SINGLE_CHAR,
             "Segment the page in \"Single character\" mode")
      .value("SPARSE_TEXT", PageSegMode::PSM_SPARSE_TEXT,
             "Segment the page in \"Sparse text\" mode")
      .value("SPARSE_TEXT_OSD", PageSegMode::PSM_SPARSE_TEXT_OSD,
             "Segment the page in \"Sparse text OSD\" mode")
      .value("RAW_LINE", PageSegMode::PSM_RAW_LINE,
             "Segment the page in \"Raw line\" mode")
      .value("COUNT", PageSegMode::PSM_COUNT,
             "Segment the page in \"Count\" mode");
}
