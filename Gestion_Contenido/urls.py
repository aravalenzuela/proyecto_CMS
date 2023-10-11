from django.urls import path
from . import views

urlpatterns = [
    path('listar_plantillas/', views.listar_plantillas, name='listar_plantillas'),
    path('seleccionar_plantilla/', views.seleccionar_plantilla, name='seleccionar_plantilla'),
]