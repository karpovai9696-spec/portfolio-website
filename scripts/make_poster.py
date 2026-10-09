# -*- coding: utf-8 -*-
"""Извлечение первого кадра hero-bg.mp4 в hero-poster.jpg (через imageio-ffmpeg)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / ".tmp-pkgs"))

import imageio.v2 as imageio

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "public" / "videos" / "hero-bg.mp4"
OUT = ROOT / "public" / "videos" / "hero-poster.jpg"

reader = imageio.get_reader(str(SRC), "ffmpeg")
frame = reader.get_data(0)
meta = reader.get_meta_data()
reader.close()

imageio.imwrite(str(OUT), frame, quality=88)
print(f"OK: {OUT} ({frame.shape[1]}x{frame.shape[0]}), fps={meta.get('fps')}, duration={meta.get('duration')}")
