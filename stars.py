#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 15:35:44 2019

@author: harrison

Based on
https://sourceforge.net/p/netpbm/code/HEAD/tree/advanced/generator/ppmforge.c
(primarily lines 433-508)

"""

from PIL import Image
import math
import random

from typing import Tuple

class Sky:
    def __init__(self, dimensions: Tuple[int, int] = (1600, 900),
                 star_fraction: float = 0.5,
                 star_quality: float = 0.5,
                 star_intensity: float = 8,
                 star_tint_exp: float = 0.5,
                 star_color: int = 125,
                 ):
        self.dimensions = dimensions
        self.image = Image.new("RGB", dimensions)
        
        self.star_fraction = star_fraction
        self.star_quality = star_quality
        self.star_intensity = star_intensity
        self.star_tint_exp = star_tint_exp
        self.star_color = star_color

    @staticmethod
    def planck(microns: float, temperature: float) -> float:
        c1 = 3.7403e10
        c2 = 14384
        return (c1 * pow(microns, -5)) / (
            pow(math.e, c2 / (microns * temperature)) - 1
        )

    @staticmethod
    def cast(low: float, high: float) -> float:
        arand = pow(2.0, 15.0) - 1.0
        return low + ((high - low) * (random.randint(0, 32767) / arand))

    def generate_star_pixel(self, temperature: float) -> Tuple[float, float, float]:
        er = self.planck(0.7, temperature)
        eg = self.planck(0.5461, temperature)
        eb = self.planck(0.4358, temperature)

        es = 1 / max(er, eg, eb)

        r = er * es
        g = eg * es
        b = eb * es

        return (r, g, b)

    def generate_sky_pixel(self) -> Tuple[int, int, int]:
        if random.random() < self.star_fraction:
            v = self.star_intensity * pow(
                1 / (1 - self.cast(0, 0.9999)), self.star_quality
            )

            if v > 255:
                v = 255

            temperature = 5500 + self.star_color * pow(
                1 / (1 - self.cast(0, 0.9999)), self.star_tint_exp
            ) * (-1 if random.randint(0, 7) else 1)
            
            # Constrain temperature to a reasonable value: >= 2600K
            # (S Cephei/R Andromedae), <= 28,000 (Spica).
            temperature = max(2600, min(28000, temperature))

            r, g, b = self.generate_star_pixel(temperature)

            r = round(r * v * 0.499)
            g = round(g * v * 0.499)
            b = round(b * v * 0.499)

            return (r, g, b)

        return (0, 0, 0)

    def generate_sky(self) -> None:
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                self.image.putpixel((x, y), self.generate_sky_pixel())


if __name__ == "__main__":
    sky = Sky()
    sky.generate_sky()
    sky.image.save("/home/harrison/Programming/stars/output.png")
