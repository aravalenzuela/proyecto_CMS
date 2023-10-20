from django.contrib import admin

# Register your models here.

from .models import Plantilla

class PlantillaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'color_principal', 'titulo_sitio']
    list_filter = ['tipo']
    search_fields = ['nombre', 'titulo_sitio']
    readonly_fields = ['color_principal', 'titulo_sitio']

admin.site.register(Plantilla, PlantillaAdmin)
