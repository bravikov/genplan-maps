from django.urls import path

import genplan.views

urlpatterns = [
    path('', genplan.views.index_page),
    path('about', genplan.views.about_page),
    path('<str:city_name>', genplan.views.city_page),
    path('<str:city_name>/<str:city_map_name>', genplan.views.city_map_page),
]
