#!/usr/bin/env python

import sys
import qrcode

if len(sys.argv) == 2:
    url = sys.argv[1]
    output = "qrcode.png"
elif len(sys.argv) == 3:
    url = sys.argv[1]
    output = sys.argv[2]
else:
    print("Usage: qrcode url [output_file]")
    exit(0)

img = qrcode.make(url)
img.save(output)
