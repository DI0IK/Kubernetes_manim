from manim import *

BG_BOX_OPACITY = 0.15

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
    label = Text(text, font_size=font_size, color="#F8F9FA", line_spacing=1.1, weight=BOLD).move_to(rect.get_center())
    return VGroup(rect, label)

def create_uniform_arrow(start, end, color="#ADB5BD"):
    return Arrow(
        start, end, 
        color=color, 
        buff=0.1, 
        stroke_width=2.5, 
        max_tip_length_to_length_ratio=0.15
    ).set_z_index(-1)

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
    t_main = Text(title, font_size=28, color="#F8F9FA", weight=BOLD).move_to(card_bg.get_center() + UP * 0.3)
    t_sub = Text(subtitle, font_size=16, color=color, weight=BOLD).move_to(card_bg.get_center() + DOWN * 0.4)
    return VGroup(card_bg, t_main, t_sub)