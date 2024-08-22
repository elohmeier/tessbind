#include <leptonica/allheaders.h>
#include <pybind11/pybind11.h>
#include <tesseract/baseapi.h>

using tesseract::PageSegMode;
using tesseract::TessBaseAPI;

int add(int i, int j) { return i + j; }

namespace py = pybind11;

PYBIND11_MODULE(_core, m) {
  m.doc() = R"pbdoc(
      Pybind11 tessbind plugin
      -----------------------
      .. currentmodule:: python_example
      .. autosummary::
         :toctree: _generate
         add
         subtract
  )pbdoc";

  m.def("add", &add, R"pbdoc(
      Add two numbers
      Some other explanation about the add function.
  )pbdoc");

  m.def("subtract", [](int i, int j) { return i - j; }, R"pbdoc(
      Subtract two numbers
      Some other explanation about the subtract function.
  )pbdoc");

  m.def("api_version", &tesseract::TessBaseAPI::Version,
        "Tesseract API version as seen in the library");

  py::class_<TessBaseAPI>(m, "TessBaseAPI")
      .def(py::init([](const char *datapath, const char *language) {
             TessBaseAPI *api = new TessBaseAPI();
             if (api->Init(datapath, language) != 0) {
               delete api;
               throw std::runtime_error("Failed to initialize Tesseract");
             }
             return std::unique_ptr<TessBaseAPI>(api);
           }),
           py::arg("datapath"), py::arg("language"))
      .def("end", &TessBaseAPI::End,
           "Close down tesseract and free up all memory, after which the "
           "instance should not be reused.")
      .def_property(
          "page_seg_mode", &TessBaseAPI::GetPageSegMode,
          &TessBaseAPI::SetPageSegMode,
          R"pbdoc(This attribute can be used to get or set the page segmentation mode used by the tesseract model)pbdoc")
      .def_property_readonly(
          "utf8_text",
          [](TessBaseAPI &api) {
            char *text = api.GetUTF8Text();
            if (!text) {
              throw std::runtime_error("Failed to get UTF8 text");
            }
            std::string result(text);
            delete[] text;
            return result;
          },
          "Return all identified text concatenated into a UTF-8 string")
      .def_property_readonly(
          "all_word_confidences", &TessBaseAPI::AllWordConfidences,
          R"pbdoc(Read-only: Return all word confidences)pbdoc")
      .def(
          "set_image_from_bytes",
          [](TessBaseAPI &api, const std::string &image_bytes) {
            Pix *image = pixReadMem((unsigned char *)image_bytes.data(),
                                    image_bytes.size());
            if (!image) {
              throw std::runtime_error("Failed to read image from bytes");
            }
            api.SetImage(image);
            pixDestroy(&image);
          },
          py::arg("image_bytes"), "Read an image from a string of bytes")
      .def(
          "recognize", [](TessBaseAPI *api) { return api->Recognize(nullptr); },
          "Recognize the text in the image set by SetImage");

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
