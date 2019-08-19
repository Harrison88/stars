from django.urls import path

from . import views

app_name = "star_generator"
urlpatterns = [
    path("", views.index, name="index"),
    path("templates", views.templates, name="templates"),
    path("generate_stars", views.generate_stars, name="generate_stars"),
]
