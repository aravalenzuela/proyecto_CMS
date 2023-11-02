from django import forms
from .models import Categoria, Rol, Permiso, Subcategoria, Usuario
from django.contrib.auth.models import User
from Gestion_Contenido.models import Plantilla


from .models import TipoDeContenido

class AsignarRolForm(forms.ModelForm):
    

    """
    Formulario para asignar un rol a un usuario.

    Args:
        usuario (Usuario): Usuario al que se le asignará el rol.

    Fields:
        rol (ModelChoiceField): Campo para seleccionar un rol de usuario.
    """
        
    class Meta:
        model = Usuario
        fields = ['rol']
        
class AsignarPermisoForm(forms.Form):

    """
    Formulario para asignar un permiso a un usuario.

    Fields:
        permiso (ModelChoiceField): Campo para seleccionar un permiso.
    """
        
    permiso = forms.ModelChoiceField(queryset=Permiso.objects.all())


class CategoriaForm(forms.ModelForm):

    """
    Formulario para crear o editar una categoría.

    Fields:
        nombre (CharField): Campo para el nombre de la categoría.
        descripcion (CharField): Campo para la descripción de la categoría.
    """
        
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

class RolForm(forms.ModelForm):

    """
    Formulario para crear o editar un rol de usuario.

    Fields:
        nombre (CharField): Campo para el nombre del rol.
        descripcion (CharField): Campo para la descripción del rol.
        permisos (ModelMultipleChoiceField): Campo para seleccionar múltiples permisos.
    """
        
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permiso.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Usamos casillas de verificación para seleccionar múltiples permisos
    )

    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion', 'permisos']



class SubcategoriaForm(forms.ModelForm):

    """
    Formulario para crear o editar una subcategoría.

    Fields:
        nombre (CharField): Campo para el nombre de la subcategoría.
        descripcion (CharField): Campo para la descripción de la subcategoría.
        categoria_relacionada (ModelChoiceField): Campo para seleccionar la categoría relacionada.
    """
        
    class Meta:
        model = Subcategoria
        fields = ['nombre', 'descripcion', 'categoria_relacionada']  # Asegúrate de que estos campos coincidan con los de tu modelo




class TipoDeContenidoForm(forms.ModelForm):
    class Meta:
        model = TipoDeContenido
        fields = ['nombre', 'descripcion', 'plantilla']

    # Añade el campo "plantilla" como un desplegable
    plantilla = forms.ModelChoiceField(
        queryset=Plantilla.objects.all(),
        empty_label="Seleccionar Plantilla",  # Etiqueta para la opción vacía
        required=False  # Para permitir que el campo sea opcional
    )


