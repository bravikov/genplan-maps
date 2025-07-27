from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap

import genplan.views


class StaticViewSitemap(sitemaps.Sitemap):
    def items(self):
        cities = genplan.views.cities_list()

        links = ['/', '/about']

        for city in cities:
            links.append(city['link'])
            for map_item in city['maps']:
                links.append(map_item['link'])

        return links

    def location(self, item):
        return item


sitemaps = {
    "static": StaticViewSitemap,
}


# При добавлении новых путей, не забудьте обновить список в StaticViewSitemap.
urlpatterns = [
    path('', genplan.views.index_page),
    path('about', genplan.views.about_page),
    path(
        'robots.txt',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
    ),

    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),

    # Пути для городов и карт должны быть последними в списке,
    # чтобы не конфликтовать с другими путями.
    path('<str:city_name>', genplan.views.city_page),
    path('<str:city_name>/<str:city_map_name>', genplan.views.city_map_page),
]
