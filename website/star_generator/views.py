from django.shortcuts import render
from django.http import HttpResponse

from .generator.stars import Sky
from io import BytesIO


def index(request):
    return render(request, "star_generator/index.html")


def generate_stars(request):
    dimensions = (int(request.POST["pixels-x"]), int(request.POST["pixels-y"]))
    star_fraction = float(request.POST['star-fraction'])
    star_quality = float(request.POST['star-quality'])
    star_intensity = float(request.POST['star-intensity'])
    star_tint_exp = float(request.POST['star-tint-exp'])
    star_color = int(request.POST['star-color'])

    starry_sky = Sky(dimensions, star_fraction, star_quality, star_intensity, star_tint_exp, star_color)
    starry_sky.generate_sky()

    bytes = BytesIO()
    starry_sky.image.save(bytes, "PNG")
    return HttpResponse(bytes.getvalue(), content_type="image/png")
