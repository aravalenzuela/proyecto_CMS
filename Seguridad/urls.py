from django.urls import path
from . import views

urlpatterns = [
    # Ruta para crear un nuevo permiso.
    path('crear_permiso/', views.crear_permiso, name='crear_permiso'),

    # Ruta para listar todos los permisos disponibles.
    path('listar_permisos/', views.listar_permisos, name='listar_permisos'),

    # Ruta para listar todos los usuarios registrados.
    path('list_users/', views.list_users, name='list_users'),

    # Ruta para crear un nuevo usuario.
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),

    # Ruta para crear una nueva categoría.
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),

    # Ruta para listar todas las categorías disponibles.
    path('listar_categorias/', views.listar_categorias, name='listar_categorias'),

    # Ruta para crear un nuevo rol.
    path('crear_rol/', views.crear_rol, name='crear_rol'),

    # Ruta para listar todos los roles.
    path('listar_roles/', views.listar_roles, name='listar_roles'),

    # Ruta para asignar permisos a los roles ya creados.
    path('asignar_permiso/', views.asignar_permiso, name='asignar_permiso'),

    path('contenidos/', views.listar_contenidos, name='lista_contenidos'),

    path('contenido/<int:pk>/', views.contenido_detalle, name='contenido_detalle'),

    # urls.py
    #path('rol/<int:rol_id>/', views.asignar_permisos_a_rol, name='asignar_permisos_a_rol'),
    #path('rol/nuevo/', views.asignar_permisos_a_rol, name='nuevo_rol'),

]
