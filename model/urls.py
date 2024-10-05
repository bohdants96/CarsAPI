from django.urls import path

from . import views

urlpatterns = [
    path("", views.manage_models, name="get_models"),
    path("<int:model_id>", views.manage_models, name="manage_models"),
]
