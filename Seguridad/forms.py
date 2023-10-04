from django import forms
from .models import Categoria, Rol, Permiso

class AsignarPermisoForm(forms.Form):
    permiso = forms.ModelChoiceField(queryset=Permiso.objects.all())
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

class RolForms(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion', 'permisos']
        widgets = {
            'permisos': forms.CheckboxSelectMultiple()  # Para seleccionar múltiples permisos
        }

class RolForm(forms.ModelForm):
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permiso.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Usamos casillas de verificación para seleccionar múltiples permisos
    )

    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion', 'permisos']
