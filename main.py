#!/usr/bin/env python3
"""Entry point: copy the pre-rendered front page to the output directory.

The image (entry.png) is the entry: a 1024x1024 newspaper front page
summing up Wednesday 25 November 2026, drawn by draw.py in this repo.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT_DIR, "entry.png"))
print("entry.png written to", OUT_DIR)
