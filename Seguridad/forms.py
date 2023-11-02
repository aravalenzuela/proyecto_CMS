from django import forms
from .models import Categoria, Rol, Permiso, Subcategoria, Usuario
from django.contrib.auth.models import User

class AsignarRolForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rol']
        
class AsignarPermisoForm(forms.Form):
    permiso = forms.ModelChoiceField(queryset=Permiso.objects.all())


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

class RolForm(forms.ModelForm):
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permiso.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Usamos casillas de verificación para seleccionar múltiples permisos
    )

    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion', 'permisos']



class SubcategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['nombre', 'descripcion', 'categoria_relacionada']  # Asegúrate de que estos campos coincidan con los de tu modelo

def clean_nombre(self):
    nombre = self.cleaned_data.get('nombre')
    if Rol.objects.filter(nombre=nombre).exists():
        raise forms.ValidationError("Este rol ya existe.")
    return nombre
