from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from Gestion_Contenido.models import Plantilla

import uuid

class Permiso(models.Model):
    """
    Modelo que representa un permiso en el sistema.

    Attributes:
        nombre (CharField): El nombre del permiso (máximo 50 caracteres).
        descripcion (CharField): Una descripción del permiso (máximo 200 caracteres).
        
    Methods:
        __str__(): Devuelve el nombre del permiso como representación en cadena.
    """

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

    nombre = models.CharField(max_length=50, unique=True)
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

    activo = models.BooleanField(default=True)  # Campo booleano para el estado de la categoría

    def __str__(self):
        return self.nombre


class TipoDeContenido(models.Model):
    """
    Modelo que representa un tipo de contenido en el sistema.
        
    Attributes:
        nombre (CharField): El nombre del tipo de contenido (máximo 100 caracteres).
        descripcion (TextField, opcional): Una descripción opcional del tipo de contenido.
        plantilla (ForeignKey a 'Gestion_Contenido.Plantilla', opcional): Una relación a una plantilla asociada (se borra en cascada si se elimina la plantilla).
        
    Methods:
        __str__(): Devuelve el nombre del tipo de contenido como representación en cadena.
    """    

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    plantilla = models.ForeignKey('Gestion_Contenido.Plantilla', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Contenido(models.Model):
    """
    Modelo que representa un contenido en el sistema.

    Attributes:
        tipo (ForeignKey a TipoDeContenido): El tipo de contenido al que pertenece este contenido.
        titulo (CharField): El título del contenido (máximo 200 caracteres).
        cuerpo (TextField): El cuerpo o contenido principal del elemento.
        fecha_creacion (DateTimeField): La fecha y hora de creación del contenido (se establece automáticamente).
        fecha_modificacion (DateTimeField): La fecha y hora de la última modificación del contenido (se actualiza automáticamente).
        autor (ForeignKey a 'auth.User'): El autor del contenido (se borra en cascada si se elimina el usuario).

    Methods:
        __str__(): Devuelve el título del contenido como representación en cadena.
    """ 
    ESTADO_BORRADOR = 'Borrador'
    ESTADO_EN_REVISION = 'En Revisión'
    ESTADO_RECHAZADO = 'Rechazado'
    ESTADO_PUBLICADO = 'Publicado'
    ESTADO_INACTIVO = 'Inactivo'

    ESTADOS_CHOICES = [
        (ESTADO_BORRADOR, 'Borrador'),
        (ESTADO_EN_REVISION, 'En Revisión'),
        (ESTADO_RECHAZADO, 'Rechazado'),
        (ESTADO_PUBLICADO, 'Publicado'),
        (ESTADO_INACTIVO, 'Inactivo'),
    ]

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado in dict(self.ESTADOS_CHOICES).keys():
            ModificacionContenido.objects.create(
                contenido=self,
                usuario_modificacion=self.autor,
                estado_anterior=self.estado,
            )
            self.estado = nuevo_estado


            # Guarda la posición solo si está cambiando a un estado diferente
            if self.estado != nuevo_estado:
                if nuevo_estado == Contenido.ESTADO_EN_REVISION:
                    self.posicion += 1
                elif nuevo_estado == Contenido.ESTADO_RECHAZADO or nuevo_estado == Contenido.ESTADO_PUBLICADO:
                    self.posicion += 2  # Ajusta según el flujo de tu tablero
                elif nuevo_estado == Contenido.ESTADO_INACTIVO:
                    self.posicion += 3  # Ajusta según el flujo de tu tablero

            # Ajusta según sea necesario

            self.save()

    tipo = models.ForeignKey(TipoDeContenido, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    cuerpo = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    plantilla = models.ForeignKey(Plantilla, on_delete=models.CASCADE, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default=ESTADO_BORRADOR)

    # Nuevo campo para la posición en el tablero Kanban
    posicion = models.IntegerField(default=0)

    comentario = models.TextField(blank=True)

    #identificador = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.titulo


# En models.py
@receiver(post_save, sender=Contenido)
def registrar_modificacion_contenido(sender, instance, created, **kwargs):
    # Registra una modificación solo si el contenido ya existía y su estado cambió
    if not created and instance.estado != instance.get_estado_display():
        ModificacionContenido.objects.create(
            contenido=instance,
            usuario_modificacion=instance.autor,
            estado_anterior=instance.estado,
        )

class Subcategoria(models.Model):

    """
    Modelo que representa una subcategoría en el sistema.

    Attributes:
        nombre (CharField): El nombre de la subcategoría (máximo 255 caracteres).
        descripcion (TextField): Una descripción de la subcategoría.
        categoria_relacionada (ForeignKey a Categoria, opcional): La categoría principal a la que está asociada la subcategoría (se borra en cascada si se elimina la categoría).

    Methods:
        __str__(): Devuelve el nombre de la subcategoría como representación en cadena.

    Example:
        Un ejemplo de un objeto Subcategoria:
        nombre = "Subcategoría 1"
        descripcion = "Una subcategoría relacionada con la Categoría A."
        categoria_relacionada = Categoria.objects.get(id=1)  # Una categoría principal asociada

    """

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    categoria_relacionada = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
  # Asegúrate de que esta línea esté presente

    def __str__(self):
        return self.nombre

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    """
    Función que crea un perfil de usuario cuando se crea un nuevo usuario.

    Parameters:
        sender (Model): El modelo que desencadenó la señal (normalmente User).
        instance (User): La instancia del usuario recién creado.
        created (bool): Indica si el usuario se ha creado recientemente.

    Returns:
        None
    """
    if created:
        Usuario.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Función que crea un perfil de usuario cuando se crea un nuevo usuario.

    Parameters:
        sender (Model): El modelo que desencadenó la señal (normalmente User).
        instance (User): La instancia del usuario recién creado.
        created (bool): Indica si el usuario se ha creado recientemente.

    Returns:
        None
    """
    
    try:
        instance.usuario.save()
    except User.usuario.RelatedObjectDoesNotExist:
        Usuario.objects.create(user=instance)




class ModificacionContenido(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    usuario_modificacion = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    estado_anterior = models.CharField(max_length=20, choices=Contenido.ESTADOS_CHOICES)
    comentario = models.TextField(blank=True, null=True)  # Ejemplo de campo de comentario
    # Otros campos para el registro de modificaciones

@receiver(post_save, sender=Contenido)
def registrar_modificacion_contenido(sender, instance, **kwargs):
    ModificacionContenido.objects.create(
        contenido=instance,
        usuario_modificacion=instance.autor,
        estado_anterior=instance.estado,
        # Otros campos para el registro de modificaciones
    )
