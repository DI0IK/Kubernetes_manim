from manim import *
from style import TEXT_LIGHT, TEXT_MUTED
import numpy as np
import qrcode

BG_BOX_OPACITY = 0.25

def create_modern_box(text, width=2.5, height=1.0, color=WHITE, font_size=18, stroke_width=2):
    rect = RoundedRectangle(
        corner_radius=0.2, 
        width=width, 
        height=height, 
        color=color, 
        stroke_width=stroke_width,
        fill_color=color, 
        fill_opacity=BG_BOX_OPACITY
    )
    label = Text(text, font_size=font_size, color=TEXT_LIGHT, line_spacing=1.1, weight=BOLD).move_to(rect.get_center())
    return VGroup(rect, label)

def create_uniform_arrow(start, end, color=TEXT_MUTED, z_index=-1):
    arrow = Arrow(
        start, end,
        color=color,
        buff=0.1,
        stroke_width=2.5,
        tip_length=0.25,
    )
    return arrow.set_z_index(z_index)


def create_uniform_double_arrow(start, end, color=TEXT_MUTED, z_index=-1):
    arrow = DoubleArrow(
        start, end,
        color=color,
        buff=0.1,
        stroke_width=2.5,
        tip_length=0.25,
    )
    return arrow.set_z_index(z_index)

def create_provider_card(title, subtitle, color):
    card_bg = RoundedRectangle(
        corner_radius=0.2, 
        width=3.2, 
        height=2.2, 
        color=color, 
        stroke_width=2, 
        fill_color=color, 
        fill_opacity=BG_BOX_OPACITY
    )
    t_main = Text(title, font_size=28, color=TEXT_LIGHT, weight=BOLD).move_to(card_bg.get_center() + UP * 0.3)
    t_sub = Text(subtitle, font_size=16, color=color, weight=BOLD).move_to(card_bg.get_center() + DOWN * 0.4)
    return VGroup(card_bg, t_main, t_sub)

def create_qr_code(url, scale=1.5):
    import numpy as np
    img = qrcode.make(url).convert("RGBA")
    return ImageMobject(np.array(img)).scale(scale)