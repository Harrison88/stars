from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .generator.stars import Sky
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
