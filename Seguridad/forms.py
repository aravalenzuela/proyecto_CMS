from django import forms
from .models import Permiso

class AsignarPermisoForm(forms.Form):
    permiso = forms.ModelChoiceField(queryset=Permiso.objects.all())
