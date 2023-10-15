from django.urls import path
from . import views

urlpatterns = [
    path('listar_plantillas/', views.listar_plantillas, name='listar_plantillas'),
    path('seleccionar_plantilla/', views.seleccionar_plantilla, name='seleccionar_plantilla'),
    path('editar_plantilla/', views.editar_plantilla, name='editar_plantilla'),  # Nueva URL
    path('profile/', views.profile_view, name='profile_view'),
    path('ver_plantilla/', views.ver_plantilla, name='ver_plantilla'),
]