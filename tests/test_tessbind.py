import tessbind


def test_add():
    assert tessbind.add(1, 2) == 3


# def test_ocr():
#     c = tessbind.Tessbind("tessdata", "eng")
#     c.SetImageFromPath("hello.png")
#     print(c.utf8Text)
