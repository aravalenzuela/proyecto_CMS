from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import hashlib
from Seguridad.models import Usuario, Rol  # Asegúrate de que este modelo exista y tenga un campo 'role'


def get_gravatar_url(email):
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s=150"

def home(request):
    return render(request, 'base.html')

def login_view(request):
    return render(request, 'login.html')

def login_with_google(oauth_code):
    # Supongamos que esta función usa oauth_code para obtener un token de Google
    # y luego inicia sesión al usuario en tu aplicación
    pass
def logout(request):
    """
    Redirecciona a la pagina de cerrar sesion de google
    :param request: HttpRequest object
    :return:HttpRedirect
    """
    return redirect('/accounts/logout/')

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
        user_role = 5  # ID del rol Lector

     # Diccionario que mapea roles a vistas
    role_to_view = {
        2: 'profile.html',
        1: 'vista_lector.html'
    }
    # Busca la vista o función correspondiente en el diccionario
    view_name = role_to_view.get(user_role, 'vista_lector.html')  # Valor predeterminado es 'profile.html'

    # Si es un nombre de vista, redirige. Si es un template, renderiza.
    if view_name.endswith('.html'):
        return render(request, view_name, {'gravatar_url': gravatar_url})
    else:
        return redirect(view_name)


def renew_session(request):
    return JsonResponse({'status': 'session renewed'})


