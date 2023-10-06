from django.db import models

from django.contrib.auth.models import User
# Create your models here.


class Plantilla(models.Model):
    TIPO_CHOICES = (
        ('blog', 'Blog (Solo texto)'),
        ('multimedia', 'Multimedia (Texto + Multimedia)'),
    )
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    contenido = models.TextField(default='Texto predeterminado')
    
    def __str__(self):
        return self.nombre
    



class PlantillaUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Aquí puedes agregar otros campos relacionados con las plantillas si es necesario

from django.db import migrations

def agregar_plantillas_ejemplo(apps, schema_editor):
    Plantilla = apps.get_model('Gestion_Contenido', 'Plantilla')
    
    # Crea las plantillas de ejemplo
    Plantilla.objects.create(nombre='Plantilla 1', tipo='blog', contenido='Contenido de la Plantilla 1')
    Plantilla.objects.create(nombre='Plantilla 2', tipo='multimedia', contenido='Contenido de la Plantilla 2')
    # Agrega más plantillas de ejemplo si es necesario

class Migration(migrations.Migration):

    dependencies = [
        # Asegúrate de que esta dependencia sea la última migración de la app Gestion_Contenido
    ]

    operations = [
        migrations.RunPython(agregar_plantillas_ejemplo),
    ]


