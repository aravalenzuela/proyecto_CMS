from django.db import models
from django.contrib.auth.models import User

class Plantilla(models.Model):
    TIPO_CHOICES = (
        ('blog', 'Blog (Solo texto)'),
        ('multimedia', 'Multimedia (Texto + Multimedia)'),
    )
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    contenido = models.TextField(default='Texto predeterminado')
    predeterminada = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre
    


class PlantillaPredeterminada(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=[('blog', 'Plantilla solo de texto'), ('imagen', 'Plantilla con imagen')])
    contenido = models.TextField()

    def __str__(self):
        return self.nombre

    

class PlantillaUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Aquí puedes agregar otros campos relacionados con las plantillas si es necesario


