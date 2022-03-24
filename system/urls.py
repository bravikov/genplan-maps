from django.urls import path, include

import genplan.views

urlpatterns = [
    path("", genplan.views.index),
    path("<str:city>", genplan.views.city_map),
]
