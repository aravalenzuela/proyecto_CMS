from django.shortcuts import render, redirect

# Create your views here.

from .models import Plantilla
from .forms import SeleccionarPlantillaForm



def listar_plantillas(request):
    plantillas = Plantilla.objects.all()
    print("Vista listar_plantillas se está ejecutando.", plantillas)
    return render(request, 'listar_plantillas.html', {'plantillas': plantillas})

def seleccionar_plantilla(request):
    if request.method == 'POST':
        form = SeleccionarPlantillaForm(request.POST)
        if form.is_valid():
            plantilla_seleccionada = form.cleaned_data['plantilla']
            # Asocia la plantilla seleccionada al usuario actual
            usuario_actual = request.user

            # Crea una instancia de PlantillaUsuario para cada plantilla seleccionada
            for plantilla in plantilla_seleccionada:#veeeer
                plantilla_usuario, created = PlantillaUsuario.objects.get_or_create(
                    usuario=usuario_actual
                )
                plantilla_usuario.plantillas.add(plantilla_seleccionada)

            return redirect('profile_view')
    else:
        form = SeleccionarPlantillaForm()

    return render(request, 'seleccionar_plantilla.html', {'form': form, 'plantillas': Plantilla.objects.all()})


from Gestion_Contenido.models import PlantillaUsuario


# ...

def profile_view(request):
    context = {}  # Define el contexto como un diccionario vacío

    # Tu lógica existente para obtener información del usuario

    # Obtener información de plantillas del usuario actual
    try:
        plantilla_usuario = PlantillaUsuario.objects.get(usuario=request.user)
        # Puedes agregar esta información al contexto para que se muestre en la plantilla
        context['plantilla_usuario'] = plantilla_usuario
    except PlantillaUsuario.DoesNotExist:
        # El usuario no tiene información de plantillas
        context['plantilla_usuario'] = None

    return render(request, 'profile.html', context)
