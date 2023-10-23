from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
class Usuario(models.Model):
    """
        Modelo utilizado para obtener los usuarios del sistema
        el modelo extiende del modelo User de Django modelo proxy
        Modelo padre : django.contrib.auth.models User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
class Categoria(models.Model):
    """
        Funcion para crear una categoría a un usuario del sistema
        
        :param1: el usuario al que sera asignado el permiso 
        :param2: el id del rol.
    """

    nombre = models.CharField(max_length=100, 
                              unique=True, 
                              error_messages= {'unique': "Ya existe una categoría con este nombre. Por favor, elige otro nombre."
        }
    )
    
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
class TipoDeContenido(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
class Contenido(models.Model):
    tipo = models.ForeignKey(TipoDeContenido, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    cuerpo = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Subcategoria(models.Model):
    
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    categoria_relacionada = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
  # Asegúrate de que esta línea esté presente

    def __str__(self):
        return self.nombre

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.usuario.save()
    except User.usuario.RelatedObjectDoesNotExist:
        Usuario.objects.create(user=instance)