from django.urls import path
from . import views
from .views import reportes_view

urlpatterns = [
    path('listar_plantillas/', views.listar_plantillas, name='listar_plantillas'),
    path('seleccionar_plantilla/', views.seleccionar_plantilla, name='seleccionar_plantilla'),
    path('editar_plantilla/', views.editar_plantilla, name='editar_plantilla'),  # Nueva URL
    path('profile/', views.profile_view, name='profile_view'),
    path('ver_plantilla/', views.ver_plantilla, name='ver_plantilla'),
    
    
    path('reportes/', views.reportes_view, name='reportes_view'),
    path('generar_reporte/', views.generar_reporte, name='generar_reporte'),  # Agrega esta línea
    #path('reportes/', views.reporte_tipos_plantillas, name='reporte_tipos_plantillas'),
    
]