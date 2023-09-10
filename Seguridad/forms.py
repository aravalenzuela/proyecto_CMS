from django import forms
from .models import Categoria, Rol, Permiso

class AsignarPermisoForm(forms.Form):
    permiso = forms.ModelChoiceField(queryset=Permiso.objects.all())
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']