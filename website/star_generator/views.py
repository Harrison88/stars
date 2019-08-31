from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .generator.stars import Sky
from .generator.templates import create_words_template
from io import BytesIO
import json

def index(request):
    return render(request, "star_generator/index.html")

def templates(request):
    return render(request, "star_generator/sky_templates.html")

@csrf_exempt
def generate_stars(request):
    values = json.loads(request.body)
    dimensions = (values.pop("pixels_x"), values.pop("pixels_y"))

    starry_sky = Sky(dimensions, **values)
    starry_sky.generate_sky()

    bytes = BytesIO()
    starry_sky.image.save(bytes, "PNG")
    return HttpResponse(bytes.getvalue(), content_type="image/png")

@csrf_exempt
def generate_stars_template(request):
    values = json.loads(request.body)
    message = values.pop("template_text")
    font_size = int(values.pop("font_size"))
    template = create_words_template(message, font_size=font_size)
    starry_sky = Sky(dimensions=template.size, template_image=template, **values)
    starry_sky.generate_sky()

    bytes= BytesIO()
    starry_sky.image.save(bytes, "PNG")
    return HttpResponse(bytes.getvalue(), content_type="image/png")
