from django.urls import path
from . import views

urlpatterns = [
    path('crear_permiso/', views.crear_permiso, name='crear_permiso'),
    path('listar_permisos/', views.listar_permisos, name='listar_permisos'),
    path('list_users/', views.list_users, name='list_users'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path('listar_categorias/', views.listar_categorias, name='listar_categorias'),
    path('crear_rol/', views.crear_rol, name='crear_rol'),
    path('listar_roles/', views.listar_roles, name='listar_roles'),
    path('asignar_permiso/', views.asignar_permiso, name='asignar_permiso'),

    # urls.py
    #path('rol/<int:rol_id>/', views.asignar_permisos_a_rol, name='asignar_permisos_a_rol'),
    #path('rol/nuevo/', views.asignar_permisos_a_rol, name='nuevo_rol'),

]
