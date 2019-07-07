from django.shortcuts import render
from django.http import HttpResponse

from .generator.stars import Sky
from io import BytesIO


def index(request):
    return render(request, 'star_generator/index.html')


def generate_stars(request):
    dimensions = (int(request.POST['pixels-x']), int(request.POST['pixels-y']))
    starry_sky = Sky(dimensions=dimensions)
    starry_sky.generate_sky()
    bytes = BytesIO()
    starry_sky.image.save(bytes, 'PNG')
    return HttpResponse(bytes.getvalue(), content_type='image/png')
