from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, white
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import io
import json
import math
import os

class CertificateGenerator:
    def __init__(self):
        self.page_width, self.page_height = A4
        self.register_fonts()
    
    def register_fonts(self):
        """注册中文字体"""
        self.font_aliases = {
            '黑体': 'SimHei',
            '宋体': 'SimSun',
            '幼圆': 'YouYuan',
            '华文楷体': 'STKaiti',
            'CJK': 'STSong',
            'SimHei': 'SimHei',
            'SimSun': 'SimSun',
            'YouYuan': 'YouYuan',
            'STKaiti': 'STKaiti',
            'STSong': 'STSong',
            'Helvetica': 'Helvetica'
        }

        self.registered_fonts = set(['Helvetica'])
        try:
            pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
            self.registered_fonts.add('STSong-Light')
        except Exception:
            pass

        base_dir = os.path.dirname(os.path.abspath(__file__))
        fonts_dir = os.path.join(base_dir, 'assets', 'fonts')
        candidates = [
            ('SimHei', ['simhei.ttf', 'SimHei.ttf', 'SimHei.TTF']),
            ('SimSun', ['simsun.ttc', 'SimSun.ttc', 'simsun.ttf', 'SimSun.ttf', 'simsunb.ttf', 'SimSunB.ttf', 'SIMSUNB.TTF']),
            ('YouYuan', ['youyuan.ttf', 'YouYuan.ttf', 'youyuan.ttc', 'YouYuan.ttc', 'SIMYOU.TTF', 'SimYou.ttf', 'simyou.ttf']),
            ('STKaiti', ['stkaiti.ttf', 'STKaiti.ttf', 'stkaiti.ttc', 'STKaiti.ttc', 'STKAITI.TTF', 'stkaiti.ttf']),
        ]

        for font_name, filenames in candidates:
            for fn in filenames:
                fp = os.path.join(fonts_dir, fn)
                if os.path.exists(fp):
                    try:
                        if fp.lower().endswith('.ttc'):
                            pdfmetrics.registerFont(TTFont(font_name, fp, subfontIndex=0))
                        else:
                            pdfmetrics.registerFont(TTFont(font_name, fp))
                        self.registered_fonts.add(font_name)
                        break
                    except Exception:
                        continue

        self.font_name = 'SimHei' if 'SimHei' in self.registered_fonts else 'Helvetica'
        self.cjk_fallback_font = 'STSong-Light' if 'STSong-Light' in self.registered_fonts else self.font_name

    def resolve_font_name(self, font_name):
        if not font_name:
            return self.font_name
        resolved = self.font_aliases.get(font_name, font_name)
        if resolved in self.registered_fonts:
            return resolved
        if self.cjk_fallback_font in self.registered_fonts:
            return self.cjk_fallback_font
        return self.font_name

    def px_to_pt(self, px):
        try:
            return float(px) * 0.75
        except Exception:
            return px

    def _px_top_to_pt_bottom(self, y_from_top_px: float, page_height_pt: float) -> float:
        return float(page_height_pt) - self.px_to_pt(y_from_top_px)

    def draw_debug_grid(self, canvas_obj, step_px=100, color=None, line_width=0.5, label=True, label_font_size=7):
        step_pt = self.px_to_pt(step_px)
        if not step_pt or step_pt <= 0:
            return

        if color is None:
            color = Color(1, 0, 0, alpha=0.25)

        canvas_obj.saveState()
        try:
            canvas_obj.setStrokeColor(color)
            canvas_obj.setFillColor(Color(1, 0, 0, alpha=0.65))
            canvas_obj.setLineWidth(line_width)

            # vertical lines
            x = 0.0
            while x <= self.page_width + 0.01:
                canvas_obj.line(x, 0, x, self.page_height)
                if label:
                    canvas_obj.setFont('Helvetica', label_font_size)
                    px_val = int(round(x / 0.75))
                    canvas_obj.drawString(x + 2, self.page_height - 10, f"x={px_val}px")
                x += step_pt

            # horizontal lines
            y = 0.0
            while y <= self.page_height + 0.01:
                canvas_obj.line(0, y, self.page_width, y)
                if label:
                    canvas_obj.setFont('Helvetica', label_font_size)
                    px_val = int(round(y / 0.75))
                    canvas_obj.drawString(2, y + 2, f"y={px_val}px")
                y += step_pt
        finally:
            canvas_obj.restoreState()

    def draw_debug_point(self, canvas_obj, x, y, radius=3.0, color=None, label=None, label_font_size=7):
        canvas_obj.saveState()
        try:
            if color is None:
                color = Color(1, 0, 0, alpha=0.9)
            canvas_obj.setStrokeColor(color)
            canvas_obj.setFillColor(color)
            # crosshair
            canvas_obj.setLineWidth(1)
            canvas_obj.line(x - radius * 2, y, x + radius * 2, y)
            canvas_obj.line(x, y - radius * 2, x, y + radius * 2)
            canvas_obj.circle(x, y, radius, stroke=1, fill=0)

            if label:
                canvas_obj.setFont('Helvetica', float(label_font_size))
                canvas_obj.drawString(x + radius * 2 + 1, y + radius * 2 + 1, str(label))
        finally:
            canvas_obj.restoreState()

    def draw_debug_box(self, canvas_obj, x, y, width, height=10, y_shift=0, color=None, line_width=0.8):
        canvas_obj.saveState()
        try:
            if color is None:
                color = Color(1, 0, 0, alpha=0.6)
            canvas_obj.setStrokeColor(color)
            canvas_obj.setLineWidth(float(line_width))
            canvas_obj.rect(x, y + y_shift, width, height, stroke=1, fill=0)
        finally:
            canvas_obj.restoreState()

    def get_field_text(self, application, field_name):
        if not field_name:
            return ""
        field_name = str(field_name).strip()

        def _norm(v):
            if v is None:
                return ""
            try:
                import math
                if isinstance(v, float) and math.isnan(v):
                    return ""
            except Exception:
                pass
            try:
                import pandas as pd
                if pd.isna(v):
                    return ""
            except Exception:
                pass
            s = str(v)
            if s.strip().lower() == 'nan':
                return ""
            return s

        # 兼容历史/第三方模板字段名：统一映射到选手姓名
        participant_field_aliases = {
            'participants_names',
            'participant_names',
            'participant_name',
            'name',
            'winner_name',
            'winners',
            'student_name',
            'student_names',
        }
        if field_name in participant_field_aliases:
            if application.participant_count > 1:
                participants = sorted(application.participants, key=lambda p: p.seq_no)
                names = [p.participant_name for p in participants]
                return "、".join(names)
            return application.participants[0].participant_name if application.participants else ""
        if field_name == 'contact_name':
            return _norm(getattr(application, 'contact_name', '') or '')
        if field_name == 'category_task':
            return _norm(f"{application.category} - {application.task}")
        if field_name == 'award_level':
            return _norm(application.award_level or "")
        if field_name == 'education_level':
            v = _norm(getattr(application, 'education_level', '') or '')
            try:
                return v[:-1] if isinstance(v, str) and v.endswith('组') else v
            except Exception:
                return v
        return _norm(getattr(application, field_name, '') or '')

    def draw_text(self, canvas_obj, text, x, y, width, font_name=None, font_size=12, align='center'):
        if text is None:
            return
        try:
            import math
            if isinstance(text, float) and math.isnan(text):
                return
        except Exception:
            pass
        text = str(text)
        if text.strip().lower() == 'nan':
            return
        font_name = self.resolve_font_name(font_name)
        font_size = float(font_size)
        canvas_obj.setFont(font_name, font_size)

        if align == 'left':
            canvas_obj.drawString(x, y, text)
            return
        if align == 'right':
            text_width = canvas_obj.stringWidth(text, font_name, font_size)
            canvas_obj.drawString(x + width - text_width, y, text)
            return

        text_width = canvas_obj.stringWidth(text, font_name, font_size)
        centered_x = x + (width - text_width) / 2
        canvas_obj.drawString(centered_x, y, text)

    def draw_wrapped_text(self, canvas_obj, text, x, y, width, font_name=None, font_size=12, align='left', line_height=None, max_lines=None, direction='up'):
        if text is None:
            return
        text = str(text)
        font_name = self.resolve_font_name(font_name)
        font_size = float(font_size)
        if line_height is None:
            line_height = font_size * 1.25

        canvas_obj.setFont(font_name, font_size)

        tokens, joiner = self._split_wrap_tokens(text)
        if not tokens:
            return

        lines = []
        current = ''
        for token in tokens:
            candidate = token if not current else f"{current}{joiner}{token}"
            if canvas_obj.stringWidth(candidate, font_name, font_size) <= width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = token
        if current:
            lines.append(current)

        if max_lines is not None:
            lines = lines[: int(max_lines)]

        for i, line in enumerate(lines):
            dy = (i * line_height) if direction == 'up' else (-i * line_height)
            self.draw_text(canvas_obj, line, x, y + dy, width, font_name=font_name, font_size=font_size, align=align)

    def _split_wrap_tokens(self, text):
        text = (text or '').strip()
        if not text:
            return [], '、'
        if '、' in text:
            tokens = [t.strip() for t in text.split('、') if t.strip()]
            return tokens, '、'
        if '，' in text:
            tokens = [t.strip() for t in text.split('，') if t.strip()]
            return tokens, '，'
        if ',' in text:
            tokens = [t.strip() for t in text.split(',') if t.strip()]
            return tokens, ', '
        if ' ' in text:
            tokens = [t.strip() for t in text.split(' ') if t.strip()]
            return tokens, ' '
        return [text], '、'

    def calculate_font_size(self, text, max_width, max_font_size=24, min_font_size=8, font_name=None):
        """
        根据文字长度和文本框宽度动态计算字号
        如果文字过长，自动缩小字号
        """
        if not text:
            return max_font_size
        
        # 从最大字号开始测试
        font_name = self.resolve_font_name(font_name)
        max_font_size = int(max_font_size)
        min_font_size = int(min_font_size)
        for font_size in range(max_font_size, min_font_size - 1, -1):
            # 设置字体并计算文字宽度
            canvas_obj = canvas.Canvas(io.BytesIO(), pagesize=A4)
            canvas_obj.setFont(font_name, font_size)
            text_width = canvas_obj.stringWidth(text, font_name, font_size)
            canvas_obj.save()
            
            # 如果文字宽度不超过最大宽度，返回当前字号
            if text_width <= max_width:
                return font_size
        
        # 如果最小字号仍然放不下，返回最小字号
        return min_font_size

    def draw_centered_text(self, canvas_obj, text, x, y, width, max_font_size=24, min_font_size=8, font_name=None):
        """
        在指定位置居中绘制文字，字号自适应
        """
        if not text:
            return
        
        # 计算合适的字号
        font_name = self.resolve_font_name(font_name)

        font_size = self.calculate_font_size(text, width, max_font_size, min_font_size, font_name=font_name)
        
        # 设置字体
        canvas_obj.setFont(font_name, font_size)
        
        # 计算文字宽度
        text_width = canvas_obj.stringWidth(text, font_name, font_size)
        
        # 计算居中位置
        centered_x = x + (width - text_width) / 2
        
        # 绘制文字
        canvas_obj.drawString(centered_x, y, text)

    def generate_certificate(self, application, template_config):
        """
        生成证书PDF
        :param application: Application对象
        :param template_config: 证书模板配置（字典格式）
        """
        # 创建PDF文件
        buffer = io.BytesIO()

        # Optional: use background PNG native size as PDF pagesize to avoid distortion.
        page_size = A4
        background_image = template_config.get('background_image')
        use_background_size = bool(template_config.get('use_background_size'))
        bg_path = None
        if background_image:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            bg_path = os.path.join(base_dir, background_image) if not os.path.isabs(background_image) else background_image
            if use_background_size and bg_path and os.path.exists(bg_path):
                try:
                    img_probe = ImageReader(bg_path)
                    iw_px, ih_px = img_probe.getSize()
                    page_size = (self.px_to_pt(iw_px), self.px_to_pt(ih_px))
                except Exception:
                    page_size = A4

        canvas_obj = canvas.Canvas(buffer, pagesize=page_size)
        old_page_w, old_page_h = self.page_width, self.page_height
        try:
            self.page_width, self.page_height = page_size

            # 绘制背景图（可选）
            if bg_path and os.path.exists(bg_path):
                try:
                    img = ImageReader(bg_path)
                    canvas_obj.drawImage(img, 0, 0, width=self.page_width, height=self.page_height, mask='auto')
                except Exception:
                    pass

            # Optional stamp overlay
            try:
                stamp_image = template_config.get('stamp_image')
                if stamp_image:
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    stamp_path = os.path.join(base_dir, stamp_image) if not os.path.isabs(str(stamp_image)) else str(stamp_image)
                    if os.path.exists(stamp_path):
                        coord_unit = str(template_config.get('coord_unit', 'mm') or 'mm').lower()
                        y_origin = str(template_config.get('y_origin', 'bottom') or 'bottom').lower()

                        def _to_pt(v):
                            if v is None:
                                return 0.0
                            if coord_unit == 'px':
                                return float(self.px_to_pt(v))
                            return float(v) * mm

                        sw = template_config.get('stamp_width')
                        sh = template_config.get('stamp_height')
                        stamp_img = ImageReader(stamp_path)
                        sw_pt = _to_pt(sw) if sw is not None else None
                        sh_pt = _to_pt(sh) if sh is not None else None
                        if sw_pt is None or sh_pt is None:
                            iw_px, ih_px = stamp_img.getSize()
                            sw_pt = sw_pt if sw_pt is not None else self.px_to_pt(iw_px)
                            sh_pt = sh_pt if sh_pt is not None else self.px_to_pt(ih_px)

                        # X position
                        stamp_center_x = bool(template_config.get('stamp_center_x'))
                        if stamp_center_x:
                            sx = (float(self.page_width) - float(sw_pt)) / 2.0
                        else:
                            sx = _to_pt(template_config.get('stamp_x', 0))

                        # Y position
                        sy_raw = float(template_config.get('stamp_y', 0) or 0)
                        sy_anchor = str(template_config.get('stamp_y_anchor', 'bottom') or 'bottom').lower()
                        if coord_unit == 'px' and y_origin == 'top':
                            sy = self._px_top_to_pt_bottom(sy_raw, self.page_height)
                        else:
                            sy = _to_pt(sy_raw)

                        # If stamp_y is a centerline, shift down by half height
                        if sy_anchor == 'center':
                            sy = float(sy) - float(sh_pt) / 2.0

                        canvas_obj.drawImage(stamp_img, sx, sy, width=sw_pt, height=sh_pt, mask='auto')
            except Exception:
                pass

            debug_grid = template_config.get('debug_grid')
            if debug_grid:
                try:
                    step_px = float(debug_grid.get('step_px', 100))
                    alpha = float(debug_grid.get('alpha', 0.25))
                    lw = float(debug_grid.get('line_width', 0.5))
                    label = bool(debug_grid.get('label', True))
                    label_font_size = float(debug_grid.get('label_font_size', 7))
                    self.draw_debug_grid(
                        canvas_obj,
                        step_px=step_px,
                        color=Color(1, 0, 0, alpha=alpha),
                        line_width=lw,
                        label=label,
                        label_font_size=label_font_size,
                    )
                except Exception:
                    pass

            debug_canvas_grid = template_config.get('debug_canvas_grid')
            if debug_canvas_grid:
                try:
                    step = float(debug_canvas_grid.get('step', 50)) * mm
                    xs = [i for i in self._frange(0, self.page_width, step)]
                    ys = [i for i in self._frange(0, self.page_height, step)]
                    canvas_obj.saveState()
                    canvas_obj.setStrokeColor(Color(1, 0, 0, alpha=float(debug_canvas_grid.get('alpha', 0.15))))
                    canvas_obj.setLineWidth(float(debug_canvas_grid.get('line_width', 0.3)))
                    canvas_obj.grid(xs, ys)
                    canvas_obj.restoreState()
                except Exception:
                    pass

            # 设置背景色（可选）
            if template_config.get('background_color'):
                canvas_obj.setFillColor(template_config['background_color'])
                canvas_obj.rect(0, 0, self.page_width, self.page_height, fill=1)

            # 设置文字颜色
            text_color = template_config.get('text_color', black)
            canvas_obj.setFillColor(text_color)

            # 新版：按texts渲染（支持固定文本/动态字段/对齐/字号）
            if template_config.get('texts'):
                coord_unit = str(template_config.get('coord_unit', 'mm') or 'mm').lower()
                y_origin = str(template_config.get('y_origin', 'bottom') or 'bottom').lower()
                global_y_offset = float(template_config.get('global_y_offset', 0)) * mm if coord_unit == 'mm' else self.px_to_pt(float(template_config.get('global_y_offset', 0) or 0))

                def _to_pt(v):
                    if v is None:
                        return 0.0
                    if coord_unit == 'px':
                        return float(self.px_to_pt(v))
                    return float(v) * mm

                debug_points = template_config.get('debug_points')
                for item in template_config.get('texts', []):
                    try:
                        width = _to_pt(item.get('width', 0))
                        x = _to_pt(item.get('x', 0))

                        raw_y = float(item.get('y', 0) or 0)
                        if coord_unit == 'px' and y_origin == 'top':
                            y = self._px_top_to_pt_bottom(raw_y, self.page_height)
                        else:
                            y = _to_pt(raw_y)

                        x_anchor = (item.get('x_anchor') or item.get('anchor') or 'left').lower()
                        if x_anchor == 'center':
                            x = x - (width / 2.0)
                        elif x_anchor == 'right':
                            x = x - width

                        y_offset_raw = float(item.get('y_offset', 0) or 0)
                        if coord_unit == 'px' and y_origin == 'top':
                            y = y + float(self.px_to_pt(y_offset_raw)) + global_y_offset
                        else:
                            y = y + _to_pt(y_offset_raw) + global_y_offset

                        align = item.get('align', 'center')
                        font = item.get('font')

                        if debug_points or item.get('debug_point'):
                            box_h = float(item.get('debug_box_height', 10))
                            box_shift = float(item.get('debug_box_y_shift', 0)) * mm
                            self.draw_debug_box(canvas_obj, x, y, width, height=box_h, y_shift=box_shift)

                        if item.get('field'):
                            txt = self.get_field_text(application, item.get('field'))
                        else:
                            txt = item.get('text', '')

                        if item.get('auto_size'):
                            max_size = self.px_to_pt(item.get('max_font_size', 16))
                            min_size = self.px_to_pt(item.get('min_font_size', 12))
                            self.draw_centered_text(canvas_obj, txt, x, y, width, max_size, min_size, font_name=font)
                        else:
                            size = self.px_to_pt(item.get('font_size', item.get('max_font_size', 16)))
                            if item.get('wrap'):
                                line_height = self.px_to_pt(item.get('line_height', None))
                                self.draw_wrapped_text(
                                    canvas_obj,
                                    txt,
                                    x,
                                    y,
                                    width,
                                    font_name=font,
                                    font_size=size,
                                    align=align,
                                    line_height=line_height,
                                    max_lines=item.get('max_lines', None),
                                    direction=item.get('direction', 'up')
                                )
                            else:
                                self.draw_text(canvas_obj, txt, x, y, width, font_name=font, font_size=size, align=align)
                    except Exception:
                        continue

                canvas_obj.save()
                buffer.seek(0)
                return buffer.getvalue()

            # Legacy blocks (mm-based). Used only when template_config does not use 'texts'.
            # 绘制证书标题
            if 'title' in template_config:
                title_config = template_config['title']
                title_font = title_config.get('font')
                self.draw_centered_text(
                    canvas_obj,
                    title_config['text'],
                    title_config['x'] * mm,
                    title_config['y'] * mm,
                    title_config['width'] * mm,
                    self.px_to_pt(title_config.get('max_font_size', 32)),
                    self.px_to_pt(title_config.get('min_font_size', 16)),
                    font_name=title_font
                )

            # 绘制获奖者姓名
            if 'name' in template_config:
                name_config = template_config['name']
                name_font = name_config.get('font')

                # 处理多人项目的姓名显示
                if application.participant_count > 1:
                    participants = sorted(application.participants, key=lambda p: p.seq_no)
                    names = [p.participant_name for p in participants]
                    name_text = "、".join(names)
                else:
                    name_text = application.participants[0].participant_name if application.participants else ""

                self.draw_centered_text(
                    canvas_obj,
                    name_text,
                    name_config['x'] * mm,
                    name_config['y'] * mm,
                    name_config['width'] * mm,
                    self.px_to_pt(name_config.get('max_font_size', 24)),
                    self.px_to_pt(name_config.get('min_font_size', 12)),
                    font_name=name_font
                )

            # 绘制学校名称
            if 'school' in template_config:
                school_config = template_config['school']
                school_font = school_config.get('font')
                self.draw_centered_text(
                    canvas_obj,
                    application.school_name,
                    school_config['x'] * mm,
                    school_config['y'] * mm,
                    school_config['width'] * mm,
                    self.px_to_pt(school_config.get('max_font_size', 20)),
                    self.px_to_pt(school_config.get('min_font_size', 10)),
                    font_name=school_font
                )

            # 绘制项目名称
            if 'project' in template_config:
                project_config = template_config['project']
                project_font = project_config.get('font')
                project_text = f"{application.category} - {application.task}"
                self.draw_centered_text(
                    canvas_obj,
                    project_text,
                    project_config['x'] * mm,
                    project_config['y'] * mm,
                    project_config['width'] * mm,
                    self.px_to_pt(project_config.get('max_font_size', 18)),
                    self.px_to_pt(project_config.get('min_font_size', 10)),
                    font_name=project_font
                )

            # 绘制获奖等级
            if 'award' in template_config:
                award_config = template_config['award']
                award_font = award_config.get('font')
                self.draw_centered_text(
                    canvas_obj,
                    application.award_level or "",
                    award_config['x'] * mm,
                    award_config['y'] * mm,
                    award_config['width'] * mm,
                    self.px_to_pt(award_config.get('max_font_size', 22)),
                    self.px_to_pt(award_config.get('min_font_size', 12)),
                    font_name=award_font
                )

            # 完成PDF绘制
            canvas_obj.save()
            buffer.seek(0)
            return buffer.getvalue()
        finally:
            self.page_width, self.page_height = old_page_w, old_page_h
    
    def create_default_template(self, category, award_level):
        """
        创建默认的证书模板配置
        """
        return {
            "background_image": None,
            "background_color": None,
            "text_color": black,
            "title": {
                "text": "获奖证书",
                "x": 50,
                "y": 200,
                "width": 100,
                "max_font_size": 32,
                "min_font_size": 16,
                "font": "黑体"
            },
            "name": {
                "x": 50,
                "y": 160,
                "width": 100,
                "max_font_size": 24,
                "min_font_size": 12,
                "font": "宋体"
            },
            "school": {
                "x": 50,
                "y": 130,
                "width": 100,
                "max_font_size": 20,
                "min_font_size": 10,
                "font": "宋体"
            },
            "project": {
                "x": 50,
                "y": 100,
                "width": 100,
                "max_font_size": 18,
                "min_font_size": 10,
                "font": "宋体"
            },
            "award": {
                "x": 50,
                "y": 70,
                "width": 100,
                "max_font_size": 22,
                "min_font_size": 12,
                "font": "华文楷体"
            }
        }

    def _frange(self, start, stop, step):
        if step <= 0:
            return
        x = float(start)
        stop = float(stop)
        step = float(step)
        while x <= stop + 1e-9:
            yield x
            x += step
