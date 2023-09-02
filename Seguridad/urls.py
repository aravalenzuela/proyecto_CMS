from django.urls import path
from . import views

urlpatterns = [
    path('crear_permiso/', views.crear_permiso, name='crear_permiso'),
    path('listar_permisos/', views.listar_permisos, name='listar_permisos')
]



