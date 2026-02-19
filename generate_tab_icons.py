from __future__ import annotations

import argparse
import os
from pathlib import Path

from PIL import Image


def _hex_to_rgba(hex_color: str) -> tuple[int, int, int, int]:
    s = hex_color.strip().lstrip("#")
    if len(s) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")
    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)
    return (r, g, b, 255)


def generate_icons(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    gray = _hex_to_rgba("9CA3AF")
    blue = _hex_to_rgba("3B82F6")

    icons = [
        ("tab-home.png", gray),
        ("tab-home-active.png", blue),
        ("tab-register.png", gray),
        ("tab-register-active.png", blue),
        ("tab-my.png", gray),
        ("tab-my-active.png", blue),
    ]

    for name, color in icons:
        img = Image.new("RGBA", (80, 80), color)
        img.save(output_dir / name, format="PNG")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        default=str(Path(os.getcwd()) / "static"),
        help="Output directory for icons (default: ./static)",
    )
    args = parser.parse_args()

    generate_icons(Path(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
