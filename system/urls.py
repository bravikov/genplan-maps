from django.urls import path, include

import genplan.views

urlpatterns = [
    path("", genplan.views.index, name="index"),
]
