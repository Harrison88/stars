#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 20:42:49 2019

@author: harrison
"""

from PIL import Image, ImageDraw, ImageFont
from matplotlib.font_manager import findSystemFonts

from typing import Union


def find_font(query: str) -> Union[str, None]:
    fonts = findSystemFonts()
    for font_path in fonts:
        if font_path.endswith(query):
            return font_path

def create_words_template(message: str,
                          font: str = 'DejaVuSerif.ttf',
                          font_size: int = 100,
                          x_padding: int = 10,
                          y_padding: int = 10,
                          ) -> Image:
    
    pil_font = ImageFont.truetype(find_font(font), font_size)
    x, y = pil_font.getsize(message)
    dimensions = (x + (x_padding * 2), y + (y_padding * 2))
    template = Image.new('RGB', dimensions)
    
    draw = ImageDraw.Draw(template)
    draw.text((x_padding, y_padding), message, (255, 255, 255), pil_font)
    
    return template