from django.urls import path

from . import views

app_name = 'star_generator'
urlpatterns = [
    path('', views.index, name='index'),
    path('generate_stars', views.generate_stars, name='generate_stars'),
]