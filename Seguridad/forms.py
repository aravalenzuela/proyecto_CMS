from django import forms
from .models import Permiso

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
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion']


#class SeleccionarPlantillaForm(forms.Form):
#    plantilla = forms.ModelChoiceField(queryset=Plantilla.objects.all())
