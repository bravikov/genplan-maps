import os

from django.http import Http404
from django.shortcuts import render
from django.template.response import TemplateResponse

from system import settings
from genplan.maps import maps_config

def get_maps(city_link):
    result_maps = []

    maps = maps_config[city_link]['maps']
    for map_link in maps:
        result_map = {
            'name': maps[map_link].name,
            'link': f'/{city_link}/{map_link}',
        }
        result_maps.append(result_map)
    return result_maps


def cities_list():
    result_cities = []
    counter = 0
    for city_link in maps_config:
        result_city = {
            'name': maps_config[city_link]['name'],
            'link': f'/{city_link}',
            'maps': get_maps(city_link),
            'id': counter
        }
        result_cities.append(result_city)
        counter += 1

    return result_cities


def index_page(request):
    result_cities = []
    counter = 0
    for city_link in maps_config:
        result_city = {
            'name': maps_config[city_link]['name'],
            'link': city_link,
            'maps': get_maps(city_link),
            'id': counter
        }
        result_cities.append(result_city)
        counter += 1

    args = {
        'cities': cities_list(),
    }
    return render(request, "index.html", args)


def city_page(request, city_name: str):
    if city_name not in maps_config:
        raise Http404("Город не найден.")

    args = {
        'title': maps_config[city_name]['name'],
        'maps': get_maps(city_name),
    }

    return TemplateResponse(request, "city.html", args)


def get_maps_storage():
    return os.environ.get('MAPS_STORAGE')


def city_map_page(request, city_name: str, city_map_name: str):
    if city_name not in maps_config:
        raise Http404("Город не найден.")

    maps = maps_config[city_name]['maps']

    if city_map_name not in maps:
        raise Http404("Карта не найдена.")

    title = maps[city_map_name].title
    if not title:
        map_name = maps[city_map_name].name
        rus_city_name = maps_config[city_name]['name']
        title = f'{map_name} – {rus_city_name}'

    args = {
        'maps_storage': get_maps_storage(),
        'map_path': maps[city_map_name].path,
        'map_title': title,
    }

    return TemplateResponse(request, "city_map.html", args)


def about_page(request):
    donate = settings.DONATE_SNIPPET
    if not donate:
        donate = 'Тут должна быть кнопка для пожертвований, но кажется ее забыли настроить.'
    return TemplateResponse(request, "about.html", {'donate': donate})
