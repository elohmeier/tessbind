{ buildPythonPackage
, pybind11
, leptonica
, tesseract5-unwrapped
, pytestCheckHook
}:

buildPythonPackage {
  pname = "tessbinding";
  version = "dev";
  src = ./.;

  nativeBuildInputs = [ pybind11 ];

  buildInputs = [
    leptonica
    tesseract5-unwrapped
  ];

  nativeCheckInputs = [
    pytestCheckHook
  ];
}
