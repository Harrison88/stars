#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 20:42:49 2019

@author: harrison
"""

from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager



def find_font() -> str:
    """Return the absolute path to a system font file.
    """
    properties = matplotlib.font_manager.FontProperties()
    return matplotlib.font_manager.findfont(properties)


def create_words_template(
    message: str,
    font: str = "DejaVuSerif.ttf",
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
    
    pil_font = ImageFont.truetype(find_font(), font_size)
    
    # To get the height of text, an instance of ImageDraw.Draw is needed.
    empty_image = Image.new("RGB", (0, 0))
    empty_draw = ImageDraw.Draw(empty_image)
    x, y = empty_draw.textsize(message, font=pil_font)
    dimensions = (x + (x_padding * 2), y + (y_padding * 2))

    template = Image.new("RGB", dimensions)
    draw = ImageDraw.Draw(template)

    draw.text((x_padding, y_padding), message, (255, 255, 255), pil_font)

    return template
