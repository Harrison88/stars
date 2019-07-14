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
    def __init__(
        self,
        dimensions: Tuple[int, int] = (900, 900),
        star_fraction: float = 0.5,
        star_quality: float = 0.5,
        star_intensity: float = 8,
        star_tint_exp: float = 0.5,
        star_color: int = 125,
        template_image: Image = None,
    ):
        """Initialize parameters to control what starry sky will be generated.
        
        Keyword arguments:
        dimensions -- the width and height of the image (default (1600, 900))
        star_fraction -- the percentage of stars in the image (default 0.5)
        star_quality -- affects the percentage of bright vs. dim stars (default 0.5)
        star_intensity -- affects the minimum brightness (default 8)
        star_tint_exp -- affects the number of stars with a higher temperature, thus causing more colorful stars (default 0.5)
        star_color -- affects the minimum temperature (default 125)
        template_image -- a PIL Image; brighter areas of the image have higher density of stars (default None)
        """
        self.dimensions = dimensions
        self.image = Image.new("RGB", dimensions)

        self.star_fraction = star_fraction
        self.star_quality = star_quality
        self.star_intensity = star_intensity
        self.star_tint_exp = star_tint_exp
        self.star_color = star_color

        if template_image is not None and template_image.size != dimensions:
            raise ValueError(
                "Size of template_image must match dimensions "
                f"for Sky image ({template_image.size} != {dimensions})"
            )

        self.template_image = template_image

    @staticmethod
    def planck(wavelength: float, temperature: float) -> float:
        """Calculate how much of a particular wavelength of light (in micrometers) a black body will emit at the given temperature.
        
        Arguments:
        wavelength -- the wavelength of light in micrometers (e.g., 0.7 for red)
        temperature -- the temperature of the black body in degrees Kelvin
        """

        c1 = 3.7403e10
        c2 = 14384
        return (c1 * pow(wavelength, -5)) / (
            pow(math.e, c2 / (wavelength * temperature)) - 1
        )

    def generate_star_pixel(self, temperature: float) -> Tuple[float, float, float]:
        """Calculate the r, g, b values for a particular temperature of a star
        
        Arguments:
        temperature -- the temperature of the star in degrees Kelvin
        """
        er = self.planck(0.7, temperature)
        eg = self.planck(0.5461, temperature)
        eb = self.planck(0.4358, temperature)

        es = 1 / max(er, eg, eb)

        r = er * es
        g = eg * es
        b = eb * es

        return (r, g, b)

    def generate_sky_pixel(self) -> Tuple[int, int, int]:
        """Calculate whether a pixel will contain a star, and if so, what temperature it will be."""
        if random.random() < self.star_fraction:
            v = self.star_intensity * pow(
                1 / (1 - random.random()), self.star_quality
            )

            if v > 255:
                v = 255

            temperature = 5500 + self.star_color * pow(
                1 / (1 - random.random()), self.star_tint_exp
            ) * (-1 if int(7 * random.random()) else 1)

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
        """Generate an image based on the parameters of the class, stored in self.image."""

        pixels = bytearray()

        for x in range(self.dimensions[1]):
            for y in range(self.dimensions[0]):

                if self.template_image is not None:
                    brightness = (
                        sum(self.template_image.getpixel((y, x))[0:3]) / 3
                    )  # Get the average of the RGB values, ignoring any possible fourth band

                    self.star_fraction = max(
                        0.2, min(0.8, brightness / 256)
                    )  # Turn brightness into a percentage between 0.2 and 0.8

                pixels.extend(self.generate_sky_pixel())

        self.image = Image.frombytes('RGB', self.dimensions, bytes(pixels))


if __name__ == "__main__":
    import templates

    template = templates.create_words_template("Hello, world!")
    sky = Sky(dimensions=template.size, template_image=template, star_intensity=16)
    sky.generate_sky()
    sky.image.save("/home/harrison/Programming/stars/output.png")
