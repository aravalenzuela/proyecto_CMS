from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Permiso, Usuario
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import AsignarPermisoForm
from .forms import CategoriaForm
from .models import Categoria  # Importación relativa


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
    permisos_a_crear = [
        {
            'nombre': 'Crear usuario',
            'descripcion': 'Permiso para crear un usuario.',
        },
        {
            'nombre': 'Consultar usuarios',
            'descripcion': 'Permiso para consultar usuarios.',
        },
        {
            'nombre': 'Dar de baja a usuario',
            'descripcion': 'Permiso para dar de baja a un usuario.',
        },
        {
            'nombre': 'Suscribirse a una categoría',
            'descripcion': 'Permiso para suscribirse a una categoría.',
        },
        {
            'nombre': 'Crear roles',
            'descripcion': 'Permiso para crear roles.',
        },
        {
            'nombre': 'Eliminar roles',
            'descripcion': 'Permiso para eliminar roles.',
        },
        {
            'nombre': 'Asignar roles a otro usuario',
            'descripcion': 'Permiso para asignar roles a otro usuario.',
        },
        {
            'nombre': 'Desasignar roles',
            'descripcion': 'Permiso para desasignar roles.',
        },
        {
            'nombre': 'Listar roles',
            'descripcion': 'Permiso para listar roles.',
        },
        {
            'nombre': 'Modificar roles',
            'descripcion': 'Permiso para modificar roles.',
        },
        {
            'nombre': 'Funciones de consultor',
            'descripcion': 'Permiso para funciones de consultor.',
        },
        {
            'nombre': 'Crear contenido',
            'descripcion': 'Permiso para crear contenido.',
        },
        {
            'nombre': 'Crear tipo de contenido',
            'descripcion': 'Permiso para crear tipo de contenido.',
        },
        {
            'nombre': 'Editar contenido',
            'descripcion': 'Permiso para editar contenido.',
        },
        {
            'nombre': 'Visualizar contenido',
            'descripcion': 'Permiso para visualizar contenido.',
        },
        {
            'nombre': 'Listar contenidos',
            'descripcion': 'Permiso para listar contenidos.',
        },
        {
            'nombre': 'Listar tipos de contenidos',
            'descripcion': 'Permiso para listar tipos de contenidos.',
        },
        {
            'nombre': 'Modificar estados del contenido',
            'descripcion': 'Permiso para modificar estados del contenido.',
        },
        {
            'nombre': 'Listar plantillas',
            'descripcion': 'Permiso para listar plantillas.',
        },
        {
            'nombre': 'Seleccionar plantilla',
            'descripcion': 'Permiso para seleccionar plantilla.',
        },
        {
            'nombre': 'Crear categorías',
            'descripcion': 'Permiso para crear categorías.',
        },
        {
            'nombre': 'Modificar categorías',
            'descripcion': 'Permiso para modificar categorías.',
        },
        {
            'nombre': 'Modificar estados de una categoría',
            'descripcion': 'Permiso para modificar estados de una categoría.',
        },
        {
            'nombre': 'Listar Categoría',
            'descripcion': 'Permiso para listar categorías.',
        },
        {
            'nombre': 'Modificar estados de una subcategoría',
            'descripcion': 'Permiso para modificar estados de una subcategoría.',
        },
        {
            'nombre': 'Crear subcategorías',
            'descripcion': 'Permiso para crear subcategorías.',
        },
        {
            'nombre': 'Modificar subcategorías',
            'descripcion': 'Permiso para modificar subcategorías.',
        },
        {
            'nombre': 'Listar subcategoría',
            'descripcion': 'Permiso para listar subcategorías.',
        },
        {
            'nombre': 'Visualizar tabla Kanban',
            'descripcion': 'Permiso para visualizar tabla Kanban.',
        },
    ]

    # Crear los permisos si no existen
    for permiso_info in permisos_a_crear:
        nombre = permiso_info['nombre']
        descripcion = permiso_info['descripcion']
        if not Permiso.objects.filter(nombre=nombre).exists():
            Permiso.objects.create(nombre=nombre, descripcion=descripcion)

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

def asignar_permiso(request, usuario_id):
    usuario = Usuario.objects.get(pk=usuario_id)
    if request.method == 'POST':
        form = AsignarPermisoForm(request.POST)
        if form.is_valid():
            permiso = form.cleaned_data['permiso']
            usuario.permisos.add(permiso)
            return redirect('listar_permisos')  # Redirige a la lista de permisos u otra vista deseada
    else:
        form = AsignarPermisoForm()
    return render(request, 'asignar_permiso.html', {'form': form, 'usuario': usuario})
# En tu views.py
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

