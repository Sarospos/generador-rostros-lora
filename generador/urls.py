from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),  # landing como página principal
    path('generar/', views.index, name='index'),
    path('galeria/', views.galeria, name='galeria'),
]