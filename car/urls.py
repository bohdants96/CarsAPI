from django.urls import path

from . import views

urlpatterns = [
    path("all/", views.get_cars, name="get_cars"),
    path("", views.manage_sale_car, name="get_sale_car"),
    path("<int:car_id>", views.manage_sale_car, name="manage_sale_car"),
]
