from django import forms
#from .models import Permiso

from .models import Plantilla

class SeleccionarPlantillaForm(forms.Form):
    plantilla = forms.ModelChoiceField(queryset=Plantilla.objects.all())