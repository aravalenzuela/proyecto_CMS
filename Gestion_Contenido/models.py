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
    color_principal = models.CharField(max_length=20, default='color_preset')# Campo para el color principal
    titulo_sitio = models.CharField(max_length=100, default='Mi Sitio Web') # Campo para el título del sitio 
    logotipo = models.ImageField(upload_to='logos/', default='default_logo.png') # Campo para el logotipo del sitio
    contenido_editable = models.TextField(blank=True, null=True)

    
    def __str__(self):
        return self.nombre
    


class PlantillaPredeterminada(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=[('blog', 'Plantilla solo de texto'), ('imagen', 'Plantilla con imagen')])
    contenido = models.TextField()

    def __str__(self):
        return self.nombre


class PlantillaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    plantillas = models.ManyToManyField(Plantilla,default="")

    def __str__(self):
        return f"Plantillas de {self.usuario.username}"




class ContenidoEditable(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    plantilla = models.ForeignKey(Plantilla, on_delete=models.CASCADE)
    contenido = models.TextField()

    def __str__(self):
        return f"Contenido editable de {self.usuario.username} para la plantilla {self.plantilla.nombre}"


    

    
