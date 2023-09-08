from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)


class Permiso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)

    def _str_(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    permisos = models.ManyToManyField(Permiso)

    def __str__(self):
        return self.nombre
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre