from django.urls import path
from . import views

urlpatterns = [
    path('crear_permiso/', views.crear_permiso, name='crear_permiso'),
    path('listar_permisos/', views.listar_permisos, name='listar_permisos'),
    path('list_users/', views.list_users, name='list_users'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('asignar_permiso/<int:usuario_id>/', views.asignar_permiso, name='asignar_permiso'),
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path('listar_categorias/', views.listar_categorias, name='listar_categorias'),

]
