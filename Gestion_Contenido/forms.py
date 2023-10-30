from django import forms

from .models import Plantilla
#from .models import Permiso

# En proyecto_CMS/Gestion_Contenido/forms.py

from .models import ContenidoEditable  # Asegúrate de importar el modelo ContenidoEditable


class PlantillaForm(forms.ModelForm):

    """
    Formulario para crear o editar una plantilla.

    Fields:
        nombre (CharField): Campo para el nombre de la plantilla.
        tipo (ChoiceField): Campo para seleccionar el tipo de plantilla.
        contenido (HiddenInput/Textarea): Campo para el contenido de la plantilla (oculto o como área de texto).
        imagen (ImageField): Campo para cargar una imagen asociada a la plantilla.
    """
        
    class Meta:
        model = Plantilla
        fields = ['nombre', 'tipo', 'contenido', 'imagen']  # Agregamos el campo 'imagen'
        widgets = {
            'tipo': forms.Select(attrs={'onchange': 'showHideFields()'}),  # Añadimos un evento onchange
        }

    def __init__(self, *args, **kwargs):
        super(PlantillaForm, self).__init__(*args, **kwargs)
        # Ocultamos el campo 'contenido' cuando el tipo es 'blog'
        self.fields['contenido'].widget = forms.HiddenInput()

        # Agregamos un atributo 'class' al campo 'contenido' para aplicar CSS personalizado
        self.fields['contenido'].widget.attrs.update({'class': 'contenido-field'})



# Agregamos un nuevo formulario para el tipo 'multimedia' que permitirá cargar imágenes
class PlantillaMultimediaForm(PlantillaForm):

    """
    Formulario para crear o editar una plantilla de tipo 'multimedia'.

    Fields:
        nombre (CharField): Campo para el nombre de la plantilla.
        tipo (ChoiceField): Campo para seleccionar el tipo de plantilla.
        contenido (Textarea): Campo para el contenido de la plantilla (como área de texto).
        imagen (ImageField): Campo para cargar una imagen asociada a la plantilla.
    """
        
    class Meta:
        model = Plantilla
        fields = ['nombre', 'tipo', 'contenido', 'imagen']

    def __init__(self, *args, **kwargs):
        super(PlantillaMultimediaForm, self).__init__(*args, **kwargs)
        # Mostramos el campo 'contenido' cuando el tipo es 'multimedia'
        self.fields['contenido'].widget = forms.Textarea(attrs={'class': 'contenido-field'})

    def is_valid(self):
        valid = super(PlantillaMultimediaForm, self).is_valid()
        if 'tipo' in self.cleaned_data and self.cleaned_data['tipo'] == 'multimedia':
            # Si el tipo es 'multimedia', asegurémonos de que se haya proporcionado una imagen
            if 'imagen' not in self.cleaned_data or not self.cleaned_data['imagen']:
                self.add_error('imagen', 'Este campo es requerido para plantillas de tipo "multimedia".')
                valid = False
        return valid




class ConfiguracionSitioForm(forms.ModelForm):

    """
    Formulario para configurar el sitio.

    Fields:
        color_principal (CharField): Campo para el color principal del sitio.
        titulo_sitio (CharField): Campo para el título del sitio.
        logotipo (ImageField): Campo para cargar un logotipo del sitio.
    """
        
    class Meta:
        model = Plantilla
        fields = ['color_principal', 'titulo_sitio', 'logotipo']



class SeleccionarPlantillaForm(forms.Form):

    """
    Formulario para seleccionar una plantilla.

    Fields:
        plantilla (ModelChoiceField): Campo para seleccionar una plantilla de sitio.
    """
        
    plantilla = forms.ModelChoiceField(queryset=Plantilla.objects.all())



class ContenidoEditableForm(forms.ModelForm):

    """
    Formulario para crear o editar contenido editable.

    Fields:
        contenido (CharField/Textarea): Campo para el contenido editable.
    """
    
    class Meta:
        model = ContenidoEditable
        fields = ['contenido']  # Asegúrate de que los campos coincidan con el modelo ContenidoEditable





