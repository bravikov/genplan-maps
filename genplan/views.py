import os
from django.shortcuts import render
from django.template.response import TemplateResponse
from urllib.parse import quote


class CityMap:
    def __init__(self, name: str, title, path):
        self.name = name
        self.title = title
        self.path = path

maps_config = {
    'kazan': {
        'name': 'Казань (от 2020)',
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
    'chelyabinsk': {
        'name': 'Челябинск',
        'maps': {
            'functional-zones-1': CityMap('Функциональные зоны',
                                          'Функциональные зоны', 'chelyabinsk-maps/functional-zones-1'),
            'functional-zones-2': CityMap('Функциональные зоны (дополнительно)',
                                          'Функциональные зоны (дополнительно)', 'chelyabinsk-maps/functional-zones-2'),
            'transport-1': CityMap('Транспорт',
                                   'Транспорт', 'chelyabinsk-maps/transport-1'),
            'transport-2': CityMap('Транспорт (дополнительно)',
                                   'Транспорт (дополнительно)', 'chelyabinsk-maps/transport-2'),
            'culture-1': CityMap('Объекты культурного наследия',
                                 'Объекты культурного наследия', 'chelyabinsk-maps/culture-1'),
            'culture-2': CityMap('Объекты культурного наследия (дополнительно)',
                                 'Объекты культурного наследия', 'chelyabinsk-maps/culture-2'),
            'garbage': CityMap('Отходы',
                               'Отходы', 'chelyabinsk-maps/garbage'),
            'social': CityMap('Социальная инфрастуктура',
                              'Социальная инфрастуктура', 'chelyabinsk-maps/social'),
            'borders': CityMap('Границы',
                               'Границы', 'chelyabinsk-maps/borders'),
            'special-zones': CityMap('Особые зоны',
                                     'Особые зоны', 'chelyabinsk-maps/special-zones'),
            'nature': CityMap('Защита от природных процессов',
                              'Защита от природных процессов', 'chelyabinsk-maps/nature'),
        },
    },
    # 'penza': {
    #     'name': 'Пенза',
    #     'maps': {
    #         '0': CityMap('Карта электро-, тепло-, газоснабжения', '', 'penza-maps/0'),
    #         '1': CityMap('Карта планируемого размещения ОКС местного значения', '', 'penza-maps/1'),
    #         '2': CityMap('Карта инженерной подготовки территории', '', 'penza-maps/2'),
    #         '3': CityMap('Карта водоотведения', '', 'penza-maps/3'),
    #         '4': CityMap('Карта функциональных зон', '', 'penza-maps/4'),
    #         '5': CityMap('Карта автомобильных дорог', '', 'penza-maps/5'),
    #         '6': CityMap('Карта границ города Пензы', '', 'penza-maps/6'),
    #     },
    # },
    'kransnodar': {
        'name': 'Краснодар (от сентября 2020)',
        'maps': {
            'functional': CityMap('Функциональные зоны', '', 'krasnodar-maps/functional'),
            'plan-education': CityMap('Планируемые образовательные объекты', '', 'krasnodar-maps/plan-education'),
            'plan-optional-education': CityMap('Планируемые объекты дополнительного образования', '', 'krasnodar-maps/plan-optional-education'),
            'plan-healthcare': CityMap('Планируемые объекты здравоохранения', '', 'krasnodar-maps/plan-healthcare'),
            'plan-green': CityMap('Планируемое озеленение', '', 'krasnodar-maps/plan-green'),
            'plan-roads': CityMap('Планируемые автомобильные дороги', '', 'krasnodar-maps/plan-roads'),
            'plan-federal-transport': CityMap('Планируемый федеральная и региональная транспортная инфраструктура', '', 'krasnodar-maps/plan-federal-transport'),
            'plan-city-transport': CityMap('Планируемый городской общественный транспорт', '', 'krasnodar-maps/plan-city-transport'),
            'plan-sport': CityMap('Планируемые спортивные объекты', '', 'krasnodar-maps/plan-sport'),
            'plan-culture': CityMap('Планируемые культурные объекты', '', 'krasnodar-maps/plan-culture'),
            'ecology': CityMap('Природно-экологический каркас', '', 'krasnodar-maps/ecology'),
            'real-healthcare': CityMap('Существующие объекты здравоохранения', '', 'krasnodar-maps/real-healthcare'),
            'real-sport': CityMap('Существующие спортивные объекты', '', 'krasnodar-maps/real-sport'),
            'real-culture': CityMap('Существующие культурные объекты', '', 'krasnodar-maps/real-culture'),
            'real-education': CityMap('Существующие образовательные объекты', '', 'krasnodar-maps/real-education'),
            'real-roads': CityMap('Современное состояние автомобильных дорог', '', 'krasnodar-maps/real-roads'),
        },
    },
    'kransnodar-2024': {
        'name': 'Краснодар (от октября 2024)',
        'maps': {
            '8': CityMap('1.2.7 Карта планируемого размещения объектов местного значения городского округа, относящихся к области автомобильных дорог', '', 'krasnodar-maps-oct-2024/8'),
            '33': CityMap('1.2.8 Карта планируемого размещения объектов местного значения городского округа, относящихся к области общественного пассажирского транспорта', '', 'krasnodar-maps-oct-2024/33'),
            '22': CityMap('1.2.9 Карта планируемого размещения объектов местного значения городского округа, относящихся к области образования', '', 'krasnodar-maps-oct-2024/22'),
            'plan-optional-education': CityMap('1.2.10 Карта планируемого размещения объектов местного значения городского округа, относящихся к области дополнительного образования', '', 'krasnodar-maps-oct-2024/0'),
            '4': CityMap('1.2.11 Карта планируемого размещения объектов местного значения городского округа, относящихся к области физической культуры и массового спорта', '', 'krasnodar-maps-oct-2024/4'),
            '11': CityMap('1.2.12 Карта планируемого размещения объектов местного значения городского округа, относящихся к областям культуры и искусства, молодежной политики, прочих объектов обслуживания', '', 'krasnodar-maps-oct-2024/11'),
            '24': CityMap('1.2.13 Карта планируемого размещения объектов местного значения городского округа, относящихся к области озеленения и особо охраняемых природных территорий', '', 'krasnodar-maps-oct-2024/24'),
            '23': CityMap('1.2.14 Карта планируемого размещения объектов местного значения городского округа, относящихся к областям инженерной защиты территории, обеспечения пожарной безопасности, организации ритуальных услуг', '', 'krasnodar-maps-oct-2024/23'),
            '18': CityMap('1.2.15 Карта границ населенных пунктов, входящих в состав городского округа', '', 'krasnodar-maps-oct-2024/18'),
            '20': CityMap('1.2.16 Карта функциональных зон городского округа', '', 'krasnodar-maps-oct-2024/20'),
            '6': CityMap('1.2.17 Карта градостроительного зонирования', '', 'krasnodar-maps-oct-2024/6'),
            '13': CityMap('1.2.18 Карта градостроительного зонирования с отображением зон с особыми условиями использования территорий', '', 'krasnodar-maps-oct-2024/13'),
            '16': CityMap('1.2.19 Карта градостроительного зонирования с отображением объектов культурного наследия', '', 'krasnodar-maps-oct-2024/16'),
            '25': CityMap('1.2.20 Карта градостроительного зонирования с отображением объектов культурного наследия. Врезка на территорию исторического поселения', '', 'krasnodar-maps-oct-2024/25'),
            '2': CityMap('1.2.22 Карта градостроительного зонирования с отображением территорий, в границах которых предусматривается осуществление комплексного развития территории', '', 'krasnodar-maps-oct-2024/2'),
            '15': CityMap('1.2.23 Карта градостроительного зонирования с отображением территорий, в границах которых предусматриваются требования к архитектурно-градостроительному облику объектов капитального строительства', '', 'krasnodar-maps-oct-2024/15'),
            '5': CityMap('2.2.1 Карта современного состояния территории', '', 'krasnodar-maps-oct-2024/5'),
            '32': CityMap('2.2.2 Карта существующих объектов социальной инфраструктуры, относящихся к области образования и науки', '', 'krasnodar-maps-oct-2024/32'),
            '17': CityMap('2.2.3 Карта существующих объектов социальной инфраструктуры, относящихся к области дополнительного образования', '', 'krasnodar-maps-oct-2024/17'),
            '3': CityMap('2.2.4 Карта существующих объектов социальной инфраструктуры, относящихся к области физической культуры и массового спорта', '', 'krasnodar-maps-oct-2024/3'),
            '27': CityMap('2.2.5 Карта существующих объектов социальной инфраструктуры, относящихся к области физической культуры и массового спорта', '', 'krasnodar-maps-oct-2024/27'),
            '29': CityMap('2.2.6 Карта существующих объектов социальной инфраструктуры, относящихся к областям здравоохранения и социального обслуживания', '', 'krasnodar-maps-oct-2024/29'),
            '30': CityMap('2.2.7 Карта размещения объектов социальной инфраструктуры, относящихся к областям образования и науки', '', 'krasnodar-maps-oct-2024/30'),
            '21': CityMap('2.2.8 Карта размещения объектов социальной инфраструктуры, относящихся к области дополнительного образования', '', 'krasnodar-maps-oct-2024/21'),
            '9': CityMap('2.2.9 Карта размещения объектов социальной инфраструктуры, относящихся к областям здравоохранения и социального обслуживания', '', 'krasnodar-maps-oct-2024/9'),
            '12': CityMap('2.2.10 Карта планируемого размещения объектов социальной инфраструктуры, относящихся к областям культуры и искусства, молодежной политики, прочих объектов обслуживания', '', 'krasnodar-maps-oct-2024/12'),
            '19': CityMap('2.2.11 Карта размещения объектов социальной инфраструктуры, относящихся к области физической культуры и массового спорта', '', 'krasnodar-maps-oct-2024/19'),
            '26': CityMap('2.2.12 Карта размещения объектов федерального, регионального, местного и иного значения', '', 'krasnodar-maps-oct-2024/26'),
            '7': CityMap('2.2.13 Карта развития транспортной инфраструктуры федерального, регионального и местного значения', '', 'krasnodar-maps-oct-2024/7'),
            '31': CityMap('2.2.14 Карта современного состояния сети автомобильных дорог общего пользования', '', 'krasnodar-maps-oct-2024/31'),
            '10': CityMap('2.2.21 Карта земель различных категорий', '', 'krasnodar-maps-oct-2024/10'),
            'zio': CityMap('2.2.22 Карта земельно-имущественных отношений', '', 'krasnodar-maps-oct-2024/1'),
            '28': CityMap('2.2.23 Карта функциональных зон с отображением зон с особыми условиями использования территорий', '', 'krasnodar-maps-oct-2024/28'),
            '14': CityMap('2.2.25 Карта природно-экологического каркаса', '', 'krasnodar-maps-oct-2024/14'),
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


def about_page(request):
    return TemplateResponse(request, "about.html")
