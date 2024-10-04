from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_models, name="get_models"),
]
