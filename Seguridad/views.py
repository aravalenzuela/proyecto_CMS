from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Permiso, Usuario , Categoria, Rol , Contenido, TipoDeContenido
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import AsignarPermisoForm
from .forms import CategoriaForm
from .models import Categoria  # Importación relativa
from .forms import CategoriaForm, RolForm
from .models import Categoria, Rol # Importación relativa

from .models import Subcategoria

from .forms import SubcategoriaForm  # Asegúrate de importar el formulario adecuado

from django.urls import reverse
#from .models import Plantilla
#from .forms import SeleccionarPlantillaForm



#Codigos para la implementacion de los requerimientos
def crear_permiso(request):
    """
    Crea un nuevo permiso y lo guarda en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de creación de permiso o redirige al perfil tras la creación exitosa.
    """
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        permiso = Permiso(nombre=nombre, descripcion=descripcion)
        permiso.save()
        return redirect('profile_view')  # Cambia esto al nombre real de la vista a la que deseas redirigir
    return render(request, 'crear_permiso.html')

def listar_permisos(request):
    """
    Lista todos los permisos disponibles en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página que muestra la lista de permisos.
    """
    permisos = Permiso.objects.all()
    return render(request, 'listar_permisos.html', {'permisos': permisos})

def list_users(request):
    """
    Lista todos los usuarios registrados en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página que muestra la lista de usuarios.
    """
    users = User.objects.all()
    return render(request, 'list_users.html', {'users': users})

def crear_usuario(request):
    """
    Crea un nuevo usuario y lo guarda en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de creación de usuario o redirige tras la creación exitosa.
    """
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
    """
    Asigna permisos a un rol específico.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        rol_id (int, optional): ID del rol al que se asignarán los permisos. Defaults to None.
        
    Returns:
        HttpResponse: Renderiza la página de asignación de permisos o redirige tras la asignación exitosa.
    """
    rol = get_object_or_404(Rol, pk=rol_id) if rol_id else None
    
    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            rol = form.save()  # Los permisos se guardarán automáticamente debido a ManyToMany
            messages.success(request, 'Permisos asignados con éxito.')
            return redirect('profile_view')
        else:
            print(form.errors)  # Agregar esta línea para imprimir los errores
            messages.error(request, 'Ha ocurrido un error al asignar los permisos.')
    else:
        form = RolForm(instance=rol)
    
    context = {
        'form': form
    }
    return render(request, 'asignar_permisos_a_rol.html', context)


def crear_categoria(request):
    """
    Crea una nueva categoría y la guarda en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de creación de categoría o redirige tras la creación exitosa.
    """
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            
            # Verificar si la categoría ya existe
            if Categoria.objects.filter(nombre=nombre).exists():
                messages.error(request, 'Esta categoría ya existe. Por favor cree una nueva')
            else:
                form.save()
                return redirect('profile_view')
    else:
        form = CategoriaForm()
    return render(request, 'crear_categoria.html', {'form': form})

def listar_categorias(request):
    """
    Lista todas las categorías disponibles en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página que muestra la lista de categorías.
    """
    categorias = Categoria.objects.all()
    return render(request, 'listar_categorias.html', {'categorias': categorias})

def crear_rol(request):
    """
    Crea un nuevo rol y lo guarda en la base de datos.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página de creación de rol o redirige tras la creación exitosa.
    """
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
    """
    Lista todos los roles disponibles en la base de datos junto con sus permisos asociados.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        
    Returns:
        HttpResponse: Renderiza la página que muestra la lista de roles.
    """
    roles = Rol.objects.all().prefetch_related('permisos')
    return render(request, 'listar_roles.html', {'roles': roles})

def listar_contenidos(request):
    contenidos = Contenido.objects.all()
    return render(request, 'lista_contenidos.html', {'contenidos': contenidos})

def contenido_detalle(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    return render(request, 'contenido_detalle.html', {'contenido': contenido})



#Mati
from django.contrib.auth.decorators import login_required

@login_required
def modificar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')  # Cambia 'listar_categorias' por el nombre real de tu vista de lista de categorías
    else:
        form = CategoriaForm(instance=categoria)
    
    context = {
        'form': form,
        'categoria': categoria,
    }
    
    return render(request, 'modificar_categoria.html', context)

def crear_subcategoria(request):
    if request.method == 'POST':
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            categoria_id = request.POST.get('categoria_relacionada')
            subcategoria_existente_id = request.POST.get('subcategoria_existente')
            nombre = form.cleaned_data.get('nombre')

            # Verificar si la subcategoría ya existe en cualquier categoría
            if Subcategoria.objects.filter(nombre=nombre).exists():
                messages.error(request, 'Esta subcategoría ya existe. Por favor, cree una nueva.')
            else:
                if categoria_id and subcategoria_existente_id:
                    # Asociar subcategoría existente con la categoría seleccionada
                    categoria = Categoria.objects.get(pk=categoria_id)
                    subcategoria_existente = Subcategoria.objects.get(pk=subcategoria_existente_id)
                    subcategoria_existente.categoria_relacionada = categoria
                    subcategoria_existente.save()
                else:
                    # Crear una nueva subcategoría
                    subcategoria = form.save(commit=False)
                    subcategoria.categoria_relacionada = Categoria.objects.get(pk=categoria_id)
                    subcategoria.save()
                    return redirect('ver_subcategoria', subcategoria_id=subcategoria.id)

    else:
        form = SubcategoriaForm()

    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all()

    return render(request, 'crear_subcategoria.html', {'form': form, 'categorias': categorias, 'subcategorias': subcategorias})



def listar_subcategorias(request):
    # Aquí coloca la lógica para obtener y listar las subcategorías desde la base de datos
    subcategorias = Subcategoria.objects.all()
    return render(request, 'listar_subcategorias.html', {'subcategorias': subcategorias})


def ver_subcategoria(request, subcategoria_id):
    subcategoria = get_object_or_404(Subcategoria, pk=subcategoria_id)
    return render(request, 'ver_subcategoria.html', {'subcategoria': subcategoria})


def modificar_subcategoria(request, subcategoria_id):
    subcategoria = Subcategoria.objects.get(pk=subcategoria_id)

    if request.method == 'POST':
        # Procesar el formulario de modificación y guardar los cambios en la base de datos
        subcategoria.nombre = request.POST['nombre']
        subcategoria.descripcion = request.POST['descripcion']
        subcategoria.save()
        return redirect(reverse('listar_subcategorias'))  # Puedes redirigir a donde desees

    return render(request, 'modificar_subcategoria.html', {'subcategoria': subcategoria})
