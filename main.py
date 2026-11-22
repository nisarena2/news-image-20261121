#!/usr/bin/env python3
"""Entry program for news-image-20261121.

Copies the front-page image held in this repository to the output
directory as entry.png. Deterministic: the same bytes every run.
The image itself is drawn by draw.py in this repository.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUT / "entry.png")


if __name__ == "__main__":
    main()
