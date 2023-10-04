from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Permiso, Usuario , Categoria, Rol 
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CategoriaForm, RolForm, AsignarPermisoForm

#Codigos para la implementacion de los requerimientos
def crear_permiso(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        permiso = Permiso(nombre=nombre, descripcion=descripcion)
        permiso.save()
        return redirect('profile_view')  # Cambia esto al nombre real de la vista a la que deseas redirigir
    return render(request, 'crear_permiso.html')

def listar_permisos(request):
    # Lista de permisos a crear
    permisos = Permiso.objects.all()
    return render(request, 'listar_permisos.html', {'permisos': permisos})

def list_users(request):
    users = User.objects.all()
    return render(request, 'list_users.html', {'users': users})

def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Puedes agregar validaciones adicionales aquí
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Usuario creado con éxito.')
            return redirect('alguna_url_donde_redirigir')
        except:
            messages.error(request, 'Ha ocurrido un error al crear el usuario.')
        
    return render(request, 'crear_usuario.html')


def asignar_permiso(request, rol_id=None): 
    rol = get_object_or_404(Rol, pk=rol_id) if rol_id else None
    
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            rol = form.save()  # Los permisos se guardarán automáticamente debido a ManyToMany
            messages.success(request, 'Permisos asignados con éxito.')
            return redirect('profile_view')
        else:
            messages.error(request, 'Ha ocurrido un error al asignar los permisos.')
    else:
        form = RolForm(instance=rol)
    
    context = {
        'form': form
    }
    return render(request, 'asignar_permisos_a_rol.html', context)


def crear_categoria(request):
    print("Método de la petición:", request.method)
    print("La función crear_categoria se ha llamado")
    if request.method == 'POST':
        print("Detectada petición POST")
        form = CategoriaForm(request.POST)
        if form.is_valid():
            print("Formulario válido")
            form.save()
            return redirect('profile_view')  # Asegúrate de que esta vista existe y está definida en tu urls.py
    else:
        print("Petición no es POST, se asume GET y se muestra formulario")
        form = CategoriaForm()
    return render(request, 'crear_categoria.html', {'form': form})

def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'listar_categorias.html', {'categorias': categorias})

def crear_rol(request):
    print("Método de la petición:", request.method)
    print("La función crear_rol se ha llamado")
    if request.method == 'POST':
        print("Detectada petición POST")
        form = RolForm(request.POST)
        if form.is_valid():
            print("Formulario válido")
            form.save()
            return redirect('profile_view')  # Asegúrate de que esta vista existe y está definida en tu urls.py
    else:
        print("Petición no es POST, se asume GET y se muestra formulario")
        form = CategoriaForm()
    return render(request, 'crear_rol.html', {'form': form})


def listar_roles(request):
    roles = Rol.objects.all().prefetch_related('permisos')
    return render(request, 'listar_roles.html', {'roles': roles})

# views.py
