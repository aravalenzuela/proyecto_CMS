from django.db import models

class Usuario(models.Model):
    """

        Modelo utilizado para obtener los usuarios del sistema
        el modelo extiende del modelo User de Django
        modelo proxy
        Modelo padre : django.contrib.auth.models User
    """
    nombre = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)


class Permiso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)

    def __str__(self):  # Asegúrate de que sea __str__ y no _str_ 
        return self.nombre
class Rol(models.Model):
    """
        Funcion para crear un rol dentro sistema
        
        :param1: el usuario al que sera aignado el permiso 
        :param2: el id del rol.
    """

    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    permisos = models.ManyToManyField(Permiso)

    def __str__(self):
        return self.nombre
    
class Categoria(models.Model):
    """
        Funcion para crear una categoría a un usuario del sistema
        
        :param1: el usuario al que sera aignado el permiso 
        :param2: el id del rol.
    """

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


#class Plantilla(models.Model):
#    nombre = models.CharField(max_length=100)
#    descripcion = models.TextField()
#
#    def __str__(self):
#        return self.nombre

#class Plantilla(models.Model):
#    TIPO_CHOICES = (
#        ('blog', 'Blog (Solo texto)'),
#        ('multimedia', 'Multimedia (Texto + Multimedia)'),
#    )
#    nombre = models.CharField(max_length=100)
#    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
#    contenido = models.TextField()
    
#    def __str__(self):
#        return self.nombre
