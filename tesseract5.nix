{ lib
, stdenv
, fetchFromGitHub
, autoreconfHook
, pkg-config
, curl
, leptonica
, libarchive
, libpng
, libtiff
, icu
, pango
, opencl-headers
, fetchpatch
, Accelerate
, CoreGraphics
, CoreVideo
}:

stdenv.mkDerivation rec {
  pname = "tesseract";
  version = "5.3.4";

  src = fetchFromGitHub {
    owner = "tesseract-ocr";
    repo = "tesseract";
    rev = version;
    sha256 = "sha256-IKxzDhSM+BPsKyQP3mADAkpRSGHs4OmdFIA+Txt084M=";
  };

  enableParallelBuilding = true;

  nativeBuildInputs = [
    pkg-config
    autoreconfHook
  ];

  buildInputs = [
    curl
    leptonica
    libarchive
    libpng
    libtiff
    icu
    pango
    opencl-headers
  ] ++ lib.optionals stdenv.isDarwin [
    Accelerate
    CoreGraphics
    CoreVideo
  ];

  makeFlags = [
    "-j10"
  ];
  installFlags = [ "DESTDIR=" ];

  buildPhase = ''
    runHook preBuild

    make $makeFlags
    make $makeFlags training
  
    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    mkdir -p $out
    make $installFlags install
    make $installFlags training-install

    runHook postInstall
  '';

  meta = {
    description = "OCR engine";
    homepage = "https://github.com/tesseract-ocr/tesseract";
    license = lib.licenses.asl20;
    maintainers = with lib.maintainers; [ anselmschueler ];
    platforms = lib.platforms.unix;
    mainProgram = "tesseract";
  };
}
