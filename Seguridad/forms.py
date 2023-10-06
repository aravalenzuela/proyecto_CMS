from django import forms
from .models import Categoria, Rol, Permiso

#from .models import Plantilla

class AsignarPermisoForm(forms.Form):
    permiso = forms.ModelChoiceField(queryset=Permiso.objects.all())
from .models import Categoria
from .models import Categoria, Rol

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
        fields = ['nombre', 'descripcion']


#class SeleccionarPlantillaForm(forms.Form):
#    plantilla = forms.ModelChoiceField(queryset=Plantilla.objects.all())
