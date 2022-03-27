import os
from django.shortcuts import render
from django.template.response import TemplateResponse


class CityMap:
    def __init__(self, name, title, path):
        self.name = name
        self.title = title
        self.path = path


maps_config = {
    'kazan': {
        'name': 'Казань',
        'maps': {
            'main': CityMap('Основной чертеж Генерального плана городского округа Казань (карта функциональных зон)',
                            'Основная карта Казань', 'kazan'),
            'borders': CityMap('Карта границ населенного пункта г. Казани', 'Границы Казань', 'kazan-maps/borders'),
        },
    },
    'gelendzhik': {
        'name': 'Геленджик',
        'maps': {
            'main': CityMap('Размещение объектов местного значения г. Геленджик', 'Объекты Геленджик', 'gelendzhik'),
        },
    },
}


def get_maps(city_link):
    result_maps = []
    maps = maps_config[city_link]['maps']
    for map_link in maps:
        result_map = {
            'name': maps[map_link].name,
            'link': f'{city_link}/{map_link}',
        }
        result_maps.append(result_map)
    return result_maps


def index_page(request):
    result_cities = []
    for city_link in maps_config:
        result_city = {
            'name': maps_config[city_link]['name'],
            'link': city_link,
            'maps': get_maps(city_link),
        }
        result_cities.append(result_city)

    args = {
        'cities': result_cities,
    }
    return render(request, "index.html", args)


def city_page(request, city_name: str):
    args = {
        'title': maps_config[city_name]['name'],
        'maps': get_maps(city_name),
    }

    return TemplateResponse(request, "city.html", args)


def get_maps_storage():
    return os.environ.get('MAPS_STORAGE')


def city_map_page(request, city_name: str, city_map_name: str):
    maps = maps_config[city_name]['maps']

    args = {
        'maps_storage': get_maps_storage(),
        'map_path': maps[city_map_name].path,
        'map_title': maps[city_map_name].title,
    }

    return TemplateResponse(request, "city_map.html", args)
