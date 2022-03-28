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
            'main': CityMap('Основная карта (функциональные зоны)',
                            'Основная карта Казань', 'kazan'),
            'borders': CityMap('Границы',
                               'Границы Казань', 'kazan-maps/borders'),
            'roads': CityMap('Дороги',
                             'Дороги Казань', 'kazan-maps/roads'),
            'social': CityMap('Объекты социальной инфраструктуры',
                              'Соц. объекты Казань', 'kazan-maps/social'),
            'electrotransport': CityMap('Электротранспорт',
                                        'Электротранспорт Казань', 'kazan-maps/electrotransport'),
            'nature': CityMap('Природно-рекреационный комплекс',
                              'Природа Казань', 'kazan-maps/nature'),
        },
    },
    'gelendzhik': {
        'name': 'Геленджик',
        'maps': {
            'main': CityMap('Геленджик: объекты',
                            'Объекты Геленджик', 'gelendzhik'),
            'gelendzhik-social': CityMap('Геленджик: объекты социальной инфраструктуры',
                                         'Геленджик: объекты социальной инфраструктуры',
                                         'gelendzhik-maps/gelendzhik-social'),
            'gelendzhik-roads': CityMap('Геленджик: дороги',
                                        'Геленджик: дороги', 'gelendzhik-maps/gelendzhik-roads'),
            'archip-osip': CityMap('Архипо-Осиповский СО: объекты',
                                   'Архипо-Осиповский СО: объекты', 'gelendzhik-maps/archip-osip'),
            'archip-osip-social': CityMap('Архипо-Осиповский СО: объекты социальной инфраструктуры',
                                          'Архипо-Осиповский СО: объекты социальной инфраструктуры',
                                          'gelendzhik-maps/archip-osip-social'),
            'divnomor': CityMap('Дивноморский СО: объекты',
                                'Дивноморский СО: объекты', 'gelendzhik-maps/divnomor'),
            'divnomor-social': CityMap('Дивноморский СО: объекты социальной инфраструктуры',
                                       'Дивноморский СО: объекты социальной инфраструктуры',
                                       'gelendzhik-maps/divnomor-social'),
            'cabardinka': CityMap('Кабардинский СО: объекты',
                                  'Кабардинский СО: объекты', 'gelendzhik-maps/cabardinka'),
            'cabardinka-social': CityMap('Кабардинский СО: объекты социальной инфраструктуры',
                                         'Кабардинский СО: объекты социальной инфраструктуры',
                                         'gelendzhik-maps/cabardinka-social'),
            'pshad': CityMap('Пшадский СО: объекты',
                             'Пшадский СО: объекты', 'gelendzhik-maps/pshad'),
            'pshad-social': CityMap('Пшадский СО: объекты социальной инфраструктуры',
                                    'Пшадский СО: объекты социальной инфраструктуры', 'gelendzhik-maps/pshad-social'),
            'mo-roads': CityMap('Муниципальное образование: дороги',
                                'МО: дороги', 'gelendzhik-maps/mo-roads'),
            'mo-engineer': CityMap('Муниципальное образование: объекты инженерной подготовки',
                                   'МО: объекты инженерной подготовки', 'gelendzhik-maps/mo-engineer'),
            'mo-transport': CityMap('Муниципальное образование: общественный транспорт',
                                    'МО: общественный транспорт', 'gelendzhik-maps/mo-transport'),
            'mo-borders': CityMap('Муниципальное образование: границы населенных пунктов',
                                  'МО: границы населенных пунктов', 'gelendzhik-maps/mo-borders'),
            'mo-zones': CityMap('Муниципальное образование: функциональное зонирования',
                                'МО: функциональное зонирования', 'gelendzhik-maps/mo-zones'),
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
