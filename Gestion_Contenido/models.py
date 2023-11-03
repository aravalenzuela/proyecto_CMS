from django.db import models
from django.contrib.auth.models import User


class Plantilla(models.Model):

    """
    Modelo que representa una plantilla de sitio web en el sistema.

    Attributes:
        TIPO_CHOICES (tuple): Las opciones para el campo 'tipo' que definen el tipo de plantilla.
        contenido (TextField): El contenido predeterminado de la plantilla.
        nombre (CharField): El nombre de la plantilla (máximo 100 caracteres).
        tipo (CharField, choices): El tipo de plantilla, que se selecciona de las opciones definidas en TIPO_CHOICES.
        predeterminada (BooleanField): Indica si esta es la plantilla predeterminada.
        color_principal (CharField): El color principal de la plantilla.
        titulo_sitio (CharField): El título del sitio web asociado a la plantilla.
        logotipo (ImageField): La imagen del logotipo del sitio web.
        contenido_editable (TextField, opcional): El contenido editable de la plantilla.
        imagen (ImageField, opcional): Una imagen asociada a la plantilla.

    Methods:
        __str__(): Devuelve el nombre de la plantilla como representación en cadena.
    """ 

    TIPO_CHOICES = (
        ('blog', 'Blog (Solo texto)'),
        ('multimedia', 'Multimedia (Texto + Multimedia)'),
    )
    contenido = models.TextField(default='Texto predeterminado')
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    predeterminada = models.BooleanField(default=False)
    color_principal = models.CharField(max_length=50, default='color_preset')# Campo para el color principal
    titulo_sitio = models.CharField(max_length=100, default='Mi Sitio Web') # Campo para el título del sitio 
    logotipo = models.ImageField(upload_to='logos/', default='default_logo.png') # Campo para el logotipo del sitio
    contenido_editable = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    


class PlantillaPredeterminada(models.Model):

    """
    Modelo que representa una plantilla predeterminada en el sistema.

    Attributes:
        nombre (CharField): El nombre de la plantilla predeterminada (máximo 100 caracteres).
        tipo (CharField, choices): El tipo de plantilla predeterminada, que se selecciona de las opciones definidas.
        contenido (TextField): El contenido predeterminado de la plantilla.

    Methods:
        __str__(): Devuelve el nombre de la plantilla predeterminada como representación en cadena.

    """

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=[('blog', 'Plantilla solo de texto'), ('imagen', 'Plantilla con imagen')])
    contenido = models.TextField()

    def __str__(self):
        return self.nombre


class PlantillaUsuario(models.Model):

    """
    Modelo que representa las plantillas seleccionadas por un usuario.

    Attributes:
        usuario (ForeignKey a User): El usuario al que pertenecen las plantillas seleccionadas.
        plantillas (ManyToManyField a Plantilla): Las plantillas seleccionadas por el usuario.

    Methods:
        __str__(): Devuelve una representación en cadena que indica las plantillas asociadas al usuario.
        
    """

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    plantillas = models.ManyToManyField(Plantilla,default="")

    def __str__(self):
        return f"Plantillas de {self.usuario.username}"




class ContenidoEditable(models.Model):

    """
    Modelo que representa el contenido editable para una plantilla de usuario.

    Attributes:
        usuario (ForeignKey a User): El usuario al que pertenece el contenido editable.
        plantilla (ForeignKey a Plantilla): La plantilla asociada al contenido editable.
        contenido (TextField): El contenido editable por el usuario.

    Methods:
        __str__(): Devuelve una representación en cadena que indica el usuario y la plantilla asociada.

    """

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    plantilla = models.ForeignKey(Plantilla, on_delete=models.CASCADE)
    contenido = models.TextField()

    def __str__(self):
        return f"Contenido editable de {self.usuario.username} para la plantilla {self.plantilla.nombre}"


    

    
