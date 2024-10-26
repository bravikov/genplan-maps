from django.urls import path
from django.views.generic.base import TemplateView

import genplan.views

urlpatterns = [
    path('', genplan.views.index_page),
    path('about', genplan.views.about_page),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path('<str:city_name>', genplan.views.city_page),
    path('<str:city_name>/<str:city_map_name>', genplan.views.city_map_page),
]
