from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/porada/losowa/', views.api_losowa_porada, name='api_losowa_porada'),
    path('api/egzaminy/', views.api_lista_egzaminow, name='api_lista_egzaminow'),
    path('api/przesady/', views.api_przesady, name='api_przesady'),
]