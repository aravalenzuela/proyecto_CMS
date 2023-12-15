from django import forms
from .models import Categoria, Rol, Permiso, Subcategoria, Usuario
from django.contrib.auth.models import User
from Gestion_Contenido.models import Plantilla
from .models import Contenido, TipoDeContenido, Plantilla


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
from django import forms
from .models import Contenido, TipoDeContenido, Plantilla

class CrearContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['titulo', 'cuerpo']  # Eliminamos 'tipo' y 'plantilla' de aquí

    def __init__(self, *args, **kwargs):
        super(CrearContenidoForm, self).__init__(*args, **kwargs)

        # Inicializa la plantilla solo si 'tipo_de_contenido' está presente
        tipo_de_contenido_id = self.data.get('tipo_de_contenido') if 'tipo_de_contenido' in self.data else None
        if tipo_de_contenido_id:
            try:
                tipo_id = int(tipo_de_contenido_id)
                tipo_de_contenido = TipoDeContenido.objects.get(id=tipo_id)
                # Aquí podrías establecer la plantilla inicial o realizar otras acciones basadas en el tipo de contenido
                # Por ejemplo, ajustar los campos del formulario según la plantilla
            except (ValueError, TypeError, TipoDeContenido.DoesNotExist):
                pass  # Manejar el error o realizar alguna acción por defecto

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
    """
    Formulario para crear o editar un tipo de contenido.

    Attributes:
        Meta (inner class):
            model (TipoDeContenido): El modelo de TipoDeContenido que se utiliza para crear el formulario.
            fields (list): Los campos del modelo que se incluirán en el formulario (nombre, descripcion, plantilla).
            
        plantilla (ModelChoiceField):
            Un campo desplegable que permite al usuario seleccionar una Plantilla para asociar al TipoDeContenido.
            El campo es opcional y tiene una etiqueta para la opción vacía.
    """
    class Meta:
        model = TipoDeContenido
        fields = ['nombre', 'descripcion', 'plantilla']

    # Añade el campo "plantilla" como un desplegable
    plantilla = forms.ModelChoiceField(
        queryset=Plantilla.objects.all(),
        empty_label="Seleccionar Plantilla",  # Etiqueta para la opción vacía
        required=False  # Para permitir que el campo sea opcional
    )

class CrearContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = ['titulo', 'cuerpo', 'imagen']  # Asegúrate de incluir 'imagen'

    def __init__(self, *args, **kwargs):
        super(CrearContenidoForm, self).__init__(*args, **kwargs)

        # Inicialización condicional basada en 'tipo_de_contenido'
        tipo_de_contenido_id = self.data.get('tipo_de_contenido') if 'tipo_de_contenido' in self.data else None
        if tipo_de_contenido_id:
            try:
                tipo_id = int(tipo_de_contenido_id)
                tipo_de_contenido = TipoDeContenido.objects.get(id=tipo_id)
                # Aquí podrías realizar ajustes adicionales en el formulario basados en el tipo de contenido
            except (ValueError, TypeError, TipoDeContenido.DoesNotExist):
                pass  # Manejar el error o realizar alguna acción por defecto