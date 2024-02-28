#!/usr/bin/env python3

from build import tessbind

import cv2

print(tessbind.add(1, 2))

img = cv2.imread("hello.png")
_, buffer = cv2.imencode(".jpg", img)

c = tessbind.Tessbind("/Users/enno/repos/tessdata_convexio/data", "eng")
c.SetImageFromBytes(buffer.tobytes())

print(c.utf8Text)
print(c.allWordConfidences)

c.SetImageFromPath("hello.png")

print(c.utf8Text)
print(c.allWordConfidences)
