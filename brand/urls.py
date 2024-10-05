from django.urls import path

from . import views

urlpatterns = [
    path("", views.manage_brands, name="get_brands"),
    path("<int:brand_id>", views.manage_brands, name="manage_brands"),
]
