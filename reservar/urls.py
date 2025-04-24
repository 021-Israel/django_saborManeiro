from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservar, name='reservar'),
    path('gravar/', views.gravar, name='gravar'),
]