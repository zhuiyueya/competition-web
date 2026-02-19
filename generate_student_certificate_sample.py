from __future__ import annotations

import os
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from certificate_generator import CertificateGenerator


@dataclass
class _Participant:
    seq_no: int
    participant_name: str


class _Application:
    def __init__(self):
        self.participant_count = 2
        self.participants = [
            _Participant(seq_no=1, participant_name="张三"),
            _Participant(seq_no=2, participant_name="李四"),
        ]
        self.category = "无人机足球"
        self.task = "机器人任务"
        self.education_level = "初中组"
        self.award_level = "一等奖"


def _px_to_pt(px: float) -> float:
    return float(px) * 0.75


def _y_from_top_px_to_reportlab(y_from_top_px: float, page_h_pt: float) -> float:
    return page_h_pt - _px_to_pt(y_from_top_px)


def _load_windows_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for p in candidates:
        try:
            if p and os.path.exists(p):
                return ImageFont.truetype(p, size)
        except Exception:
            continue
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()


def _draw_centered_in_box(draw: ImageDraw.ImageDraw, text: str, box: tuple[float, float, float, float], font):
    x, y, w, h = box
    if text is None:
        return
    text = str(text)
    if not text.strip():
        return

    # Center both horizontally and vertically inside the box.
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = x + (w - tw) / 2
    ty = y + (h - th) / 2
    draw.text((tx, ty), text, fill=(0, 0, 0, 255), font=font)


def render_png_preview(bg_path: str, out_path: str, app: _Application, gen: CertificateGenerator) -> None:
    img = Image.open(bg_path).convert("RGBA")
    w, h = img.size
    draw = ImageDraw.Draw(img)

    base_font_px = 24

    # Try to load real Windows fonts first.
    win_fonts_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
    song_candidates = [
        os.path.join(win_fonts_dir, "simsun.ttc"),
        os.path.join(win_fonts_dir, "SimSun.ttc"),
        os.path.join(win_fonts_dir, "simsun.ttf"),
        os.path.join(win_fonts_dir, "SimSun.ttf"),
    ]
    kaiti_candidates = [
        os.path.join(win_fonts_dir, "STKAITI.TTF"),
        os.path.join(win_fonts_dir, "stkaiti.ttf"),
        os.path.join(win_fonts_dir, "simkai.ttf"),
        os.path.join(win_fonts_dir, "SIMKAI.TTF"),
    ]

    font_song_16 = _load_windows_font(song_candidates, base_font_px)
    font_kaiti_84 = _load_windows_font(kaiti_candidates, 84)

    # Boxes are in pixels, origin top-left.
    name_box = (0, 400, w, 28)
    category_box = (680, 460, 860 - 680, 28)
    group_box = (920, 460, 1060 - 920, 28)
    award_box = (0, 540, w, 100)

    name_text = gen.get_field_text(app, "participants_names")
    category_text = gen.get_field_text(app, "category")
    group_text = gen.get_field_text(app, "education_level")
    award_text = gen.get_field_text(app, "award_level")

    try:
        if isinstance(group_text, str) and group_text.endswith("组"):
            group_text = group_text[:-1]
    except Exception:
        pass

    _draw_centered_in_box(draw, name_text, name_box, font_song_16)
    _draw_centered_in_box(draw, category_text, category_box, font_song_16)
    _draw_centered_in_box(draw, group_text, group_box, font_song_16)
    _draw_centered_in_box(draw, award_text, award_box, font_kaiti_84)

    img.save(out_path, "PNG")


def main() -> int:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bg_rel = os.path.join("assets", "cert", "player.png")
    bg_path = os.path.join(base_dir, bg_rel)
    if not os.path.exists(bg_path):
        raise FileNotFoundError(bg_path)

    img = ImageReader(bg_path)
    iw_px, ih_px = img.getSize()  # pixels

    # 1px = 0.75pt to match CertificateGenerator.px_to_pt
    page_w_pt = _px_to_pt(iw_px)
    page_h_pt = _px_to_pt(ih_px)

    out_path = os.path.join(base_dir, "student_certificate_sample.pdf")
    c = canvas.Canvas(out_path, pagesize=(page_w_pt, page_h_pt))

    # background
    c.drawImage(img, 0, 0, width=page_w_pt, height=page_h_pt, mask="auto")

    gen = CertificateGenerator()
    app = _Application()

    png_out_path = os.path.join(base_dir, "student_certificate_sample.png")
    render_png_preview(bg_path, png_out_path, app, gen)

    # ===== Fields (all centered within given boxes) =====
    base_font_px = 24
    # Name: y=400 (from top), full width
    name_x_px, name_w_px = 0, iw_px
    name_y_px = 400

    # Category (赛别): x 680-860, y 460-480 -> use midline y=470
    cat_x_px, cat_w_px = 680, 860 - 680
    cat_y_px = (460 + 480) / 2

    # Group (组别): x 920-1060, y 460-480 -> use midline y=470
    grp_x_px, grp_w_px = 920, 1060 - 920
    grp_y_px = (460 + 480) / 2

    # Award level: y 540-640 -> use midline y=590, full width
    award_x_px, award_w_px = 0, iw_px
    award_y_px = (540 + 640) / 2

    # Resolve dynamic texts
    name_text = gen.get_field_text(app, "participants_names")
    category_text = gen.get_field_text(app, "category")
    group_text = gen.get_field_text(app, "education_level")
    award_text = gen.get_field_text(app, "award_level")

    try:
        if isinstance(group_text, str) and group_text.endswith("组"):
            group_text = group_text[:-1]
    except Exception:
        pass

    # Draw
    gen.draw_text(
        c,
        name_text,
        _px_to_pt(name_x_px),
        _y_from_top_px_to_reportlab(name_y_px, page_h_pt),
        _px_to_pt(name_w_px),
        font_name="宋体",
        font_size=_px_to_pt(base_font_px),
        align="center",
    )

    gen.draw_text(
        c,
        category_text,
        _px_to_pt(cat_x_px),
        _y_from_top_px_to_reportlab(cat_y_px, page_h_pt),
        _px_to_pt(cat_w_px),
        font_name="宋体",
        font_size=_px_to_pt(base_font_px),
        align="center",
    )

    gen.draw_text(
        c,
        group_text,
        _px_to_pt(grp_x_px),
        _y_from_top_px_to_reportlab(grp_y_px, page_h_pt),
        _px_to_pt(grp_w_px),
        font_name="宋体",
        font_size=_px_to_pt(base_font_px),
        align="center",
    )

    gen.draw_text(
        c,
        award_text,
        _px_to_pt(award_x_px),
        _y_from_top_px_to_reportlab(award_y_px, page_h_pt),
        _px_to_pt(award_w_px),
        font_name="华文楷体",
        font_size=_px_to_pt(84),
        align="center",
    )

    c.showPage()
    c.save()

    print(f"Saved: {out_path}")
    print(f"Saved: {png_out_path}")
    print(f"Canvas size (px): {iw_px}x{ih_px}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
