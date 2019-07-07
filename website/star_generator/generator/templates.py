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
    """Return the absolute path to a system font file.
    
    Arguments:
    query -- the font file name (e.g., 'DejaVuSerif.ttf')
    """
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
    """Returns an Image containing white words on black background.
    
    This Image is suitable for being passed to a Sky class as a template_image.
    
    Arguments:
    message -- the words to be written
    font -- the name of the font file to be loaded (default 'DejaVuSerif.ttf')
    font_size -- the size of the font (default 100)
    x_padding -- the number of pixels to the left and right of the words
    y_padding -- the number of pixels above and below the words
    """
    pil_font = ImageFont.truetype(find_font(font), font_size)
    x, y = pil_font.getsize(message)
    dimensions = (x + (x_padding * 2), y + (y_padding * 2))
    template = Image.new('RGB', dimensions)
    
    draw = ImageDraw.Draw(template)
    draw.text((x_padding, y_padding), message, (255, 255, 255), pil_font)
    
    return template