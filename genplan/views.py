from django.shortcuts import render
from django.template.response import TemplateResponse


def index(request):
    return render(request, "index.html")


def city_map(request, city: str):
    args = {
        'city': city,
    }
    return TemplateResponse(request, "city_map.html", args)
