from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.get_cars, name='get_cars'),
    path('', views.get_sale_cars, name='get_sale_cars'),
]