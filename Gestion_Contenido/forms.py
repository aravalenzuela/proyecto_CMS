from django import forms

from .models import Plantilla
#from .models import Permiso

# En proyecto_CMS/Gestion_Contenido/forms.py

class PlantillaForm(forms.ModelForm):
    class Meta:
        model = Plantilla
        fields = ['nombre', 'tipo', 'contenido']



class SeleccionarPlantillaForm(forms.Form):
    plantilla = forms.ModelChoiceField(queryset=Plantilla.objects.all())

