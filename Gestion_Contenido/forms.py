from django import forms

from .models import Plantilla
#from .models import Permiso

# En proyecto_CMS/Gestion_Contenido/forms.py

from .models import ContenidoEditable  # Asegúrate de importar el modelo ContenidoEditable

class PlantillaForm(forms.ModelForm):
    class Meta:
        model = Plantilla
        fields = ['nombre', 'tipo', 'contenido']


class ConfiguracionSitioForm(forms.ModelForm):
    class Meta:
        model = Plantilla
        fields = ['color_principal', 'titulo_sitio', 'logotipo']

class SeleccionarPlantillaForm(forms.Form):
    plantilla = forms.ModelChoiceField(queryset=Plantilla.objects.all())



class ContenidoEditableForm(forms.ModelForm):
    class Meta:
        model = ContenidoEditable
        fields = ['contenido']  # Asegúrate de que los campos coincidan con el modelo ContenidoEditable





