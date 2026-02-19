from __future__ import annotations

import argparse
import os
from PIL import Image, ImageDraw, ImageFont


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        # Pillow usually bundles DejaVu fonts; fall back to default if not available.
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()


def overlay_grid(
    input_path: str,
    output_path: str,
    minor_step: int = 20,
    major_step: int = 100,
) -> None:
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    minor_color = (255, 0, 0, 60)
    major_color = (255, 0, 0, 140)

    # Minor grid
    for x in range(0, w, minor_step):
        draw.line([(x, 0), (x, h)], fill=minor_color, width=1)
    for y in range(0, h, minor_step):
        draw.line([(0, y), (w, y)], fill=minor_color, width=1)

    # Major grid + labels
    font = _load_font(16)
    label_bg = (255, 255, 255, 180)

    def draw_label(x: int, y: int, text: str) -> None:
        tw, th = draw.textbbox((0, 0), text, font=font)[2:]
        pad = 3
        draw.rectangle([x, y, x + tw + pad * 2, y + th + pad * 2], fill=label_bg)
        draw.text((x + pad, y + pad), text, fill=(255, 0, 0, 220), font=font)

    for x in range(0, w, major_step):
        draw.line([(x, 0), (x, h)], fill=major_color, width=3)
        if x != 0:
            draw_label(min(x + 2, w - 60), 2, str(x))

    for y in range(0, h, major_step):
        draw.line([(0, y), (w, y)], fill=major_color, width=3)
        if y != 0:
            draw_label(2, min(y + 2, h - 30), str(y))

    out = Image.alpha_composite(img, overlay).convert("RGBA")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    out.save(output_path, "PNG")


def main() -> int:
    parser = argparse.ArgumentParser(description="Overlay red grid on a PNG certificate template.")
    parser.add_argument(
        "--input",
        default=os.path.join("assets", "cert", "player.png"),
        help="Input template PNG path",
    )
    parser.add_argument(
        "--output",
        default="template_with_grid.png",
        help="Output PNG path",
    )
    parser.add_argument("--minor", type=int, default=20, help="Minor grid step in pixels")
    parser.add_argument("--major", type=int, default=100, help="Major grid step in pixels")
    args = parser.parse_args()

    overlay_grid(args.input, args.output, minor_step=args.minor, major_step=args.major)
    print(f"Saved: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
