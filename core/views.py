from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import hashlib
from Seguridad.models import Usuario, Rol, Notificacion  # Asegúrate de que este modelo exista y tenga un campo 'role'
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout


def get_gravatar_url(email):
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s=150"

@cache_control(no_cache=True, must_revalidate=True, no_store=True) #Limpia Cache para no redirigir
def home(request):
    return render(request, 'base.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    return render(request, 'login.html')

def login_with_google(oauth_code):
    # Supongamos que esta función usa oauth_code para obtener un token de Google
    # y luego inicia sesión al usuario en tu aplicación
    pass

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    """
    Redirecciona a la pagina de cerrar sesion de google
    :param request: HttpRequest object
    :return:HttpRedirect
    """
    logout(request)  # Cierra la sesión del usuario
    return redirect('/accounts/logout/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile_view(request):
    # Verifica si el usuario está autenticado
    if not request.user.is_authenticated:
        return redirect('login_view')  # Redirige al usuario a la vista de inicio de sesión

    # Obtiene el email del usuario y su avatar
    user_email = request.user.email
    gravatar_url = get_gravatar_url(user_email)

    # Obtiene el perfil del usuario y su rol
    try:
        user_profile = Usuario.objects.get(user=request.user)
        user_role = user_profile.rol.id if user_profile.rol else None
    except Usuario.DoesNotExist:
        # Si el usuario no tiene un perfil, crea uno y le asigna el rol de lector
        lector_role = Rol.objects.get(id=5)
        user_profile = Usuario.objects.create(user=request.user, rol=lector_role)
        user_role = 2  # ID del rol suscriptor

     # Diccionario que mapea roles a vistas
    role_to_view = {
        1: 'profile.html',
        2: 'vista_suscriptor.html',
        3: 'vista_autor.html',
        4: 'vista_editores.html',
        5: 'vista_publicador.html'
    }
    # Busca la vista o función correspondiente en el diccionario
    view_name = role_to_view.get(user_role, 'vista_suscriptor.html')  # Valor predeterminado es 'profile.html'

    # Si es un nombre de vista, redirige. Si es un template, renderiza.
    if view_name.endswith('.html'):
        return render(request, view_name, {'gravatar_url': gravatar_url})
    else:
        return redirect(view_name)


def notificaciones_view(request):
    """
    Vista para mostrar las notificaciones de un usuario.

    Parameters:
    - request: Objeto HttpRequest.

    Returns:
    - HttpResponse: Renderiza la página de notificaciones.
    """
    if not request.user.is_authenticated:
        return redirect('login_view')  # Redirige al usuario a la vista de inicio de sesión si no está autenticado

    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    context = {'notificaciones': notificaciones}

    return render(request, 'notificaciones.html', context)

def renew_session(request):
    return JsonResponse({'status': 'session renewed'})

#Paneles de Roles
def panel_autor(request):
    # Asumiendo que tienes un template llamado 'panel_autor.html'
    return render(request, 'panel_autor.html', {}, content_type='text/html')

def panel_editores(request):
    # Asumiendo que tienes un template llamado 'panel_autor.html'
    return render(request, 'panel_editores.html', {}, content_type='text/html')

def panel_publicador(request):
    # Asumiendo que tienes un template llamado 'panel_autor.html'
    return render(request, 'panel_publicador.html', {}, content_type='text/html')

def panel_suscriptor(request):
    # Asumiendo que tienes un template llamado 'panel_autor.html'
    return render(request, 'panel_suscriptor.html', {}, content_type='text/html')

def vista_contenido(request):
    """
    Vista que muestra los contenidos organizados por estado.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la página de la vista de cada usuario
    """
    from Seguridad.models import Contenido
    estados = [estado[0] for estado in Contenido.ESTADOS_CHOICES]
    contenidos_por_estado = {estado: Contenido.objects.filter(estado=estado).order_by('posicion') for estado in estados}
    print("Contenidos por estado:", contenidos_por_estado)  # Esto imprimirá el valor en la consola del servidor
    print([estado[0] for estado in Contenido.ESTADOS_CHOICES])  # Esto te mostrará todos los estados posibles.
     # Imprime los estados y sus contenidos asociados
    for estado, contenidos in contenidos_por_estado.items():
        print("Estado:", estado)
        for contenido in contenidos:
            print("Contenido:", contenido.titulo, contenido.estado)
    print(contenidos_por_estado)
    return render(request, 'vista_autor.html', {'contenidos_por_estado': contenidos_por_estado})