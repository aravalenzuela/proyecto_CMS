from django.http import HttpResponse
from django.shortcuts import redirect, render
import hashlib

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
    if not request.user.is_authenticated:
        return redirect('login_view')  # Redirige al usuario a la vista de inicio de sesión

    user_email = request.user.email
    gravatar_url = get_gravatar_url(user_email)
    return render(request, 'profile.html', {'gravatar_url': gravatar_url})
