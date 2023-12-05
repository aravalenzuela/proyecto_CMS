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

   # Ruta para modificar el estado de una categoría.
    path('modificar_estado_categoria/<int:categoria_id>/', views.modificar_estado_categoria, name='modificar_estado_categoria'),   

    # Ruta para crear un nuevo rol.
    path('crear_rol/', views.crear_rol, name='crear_rol'),

    # Ruta para listar todos los roles.
    path('listar_roles/', views.listar_roles, name='listar_roles'),

    # Ruta para asignar permisos a los roles ya creados.
    path('asignar_permiso/', views.asignar_permiso, name='asignar_permiso'),

    path('listar_contenidos/', views.listar_contenidos, name='listar_contenidos'),

    path('contenido/<int:pk>/', views.contenido_detalle, name='contenido_detalle'),
    # Ruta para modificar una categoría existente.
    path('modificar_categoria/', views.modificar_categoria, name='modificar_categoria'),

    # URL para crear una subcategoría
    path('crear_subcategoria/', views.crear_subcategoria, name='crear_subcategoria'),

    path('listar_subcategorias/', views.listar_subcategorias, name='listar_subcategorias'),

    path('ver_subcategoria/<int:subcategoria_id>/', views.ver_subcategoria, name='ver_subcategoria'),

    path('Modificar_Subcategoria/<int:subcategoria_id>/', views.modificar_subcategoria, name='modificar_subcategoria'),

    path('asignar_rol/<int:usuario_id>/', views.asignar_rol_a_usuario, name='asignar_rol_a_usuario'),

    path('vista_lector/', views.vista_lector, name="vista_lector"),

    path('dar_de_baja_o_activar/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),

    path('eliminar_rol/<int:rol_id>/', views.eliminar_rol, name='eliminar_rol'),

    path('modificar_rol/<int:rol_id>/', views.modificar_rol, name='modificar_rol'),

    path('crear_tipo_de_contenido/', views.crear_tipo_de_contenido, name='crear_tipo_de_contenido'),
    
    path('listar_tipos_de_contenido/', views.listar_tipos_de_contenido, name='listar_tipos_de_contenido'),
    
    path('crear_contenido/', views.crear_contenido, name='crear_contenido'),
    #path('crear_contenido/obtener_todas_las_plantillas/', views.obtener_todas_las_plantillas, name='obtener_todas_las_plantillas'),


    
    path('contenido/<int:contenido_id>/revisar/', views.revisar_contenido, name='revisar_contenido'),
    path('contenido/<int:contenido_id>/aprobar/', views.aprobar_contenido, name='aprobar_contenido'),
    path('contenido/<int:contenido_id>/desaprobar/', views.desaprobar_contenido, name='desaprobar_contenido'),
    path('contenido/<int:contenido_id>/inactivar/', views.inactivar_contenido, name='inactivar_contenido'),
    path('contenido/<int:contenido_id>/cancelar/', views.cancelar_agregar_contenido, name='cancelar_agregar_contenido'),
    path('contenido/<int:contenido_id>/', views.detalle_contenido, name='detalle_contenido'),
    path('tablero_kanban/', views.tablero_kanban, name='tablero_kanban'),
    
    path('cambiar_estado/', views.cambiar_estado_contenido, name='cambiar_estado_contenido'),

    path('agregar_like/<int:contenido_id>/', views.agregar_like, name='agregar_like'),
    path('agregar_comentario/<int:contenido_id>/', views.agregar_comentario, name='agregar_comentario'),
    path('agregar_respuesta/<int:comentario_id>/', views.agregar_respuesta, name='agregar_respuesta'),
    path('compartir_contenido/<int:contenido_id>/', views.compartir_contenido, name='compartir_contenido'),
    path('obtener_notificaciones/', views.obtener_notificaciones, name='obtener_notificaciones'),
]

