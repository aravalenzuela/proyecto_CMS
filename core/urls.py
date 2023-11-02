"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'), #Inicio del Home - http://127.0.0.1:8000/
    path('admin/', admin.site.urls),#funciond el admin - http://127.0.0.1:8000/admin   
    path('login/', views.login_view, name='login'),  # Inicio del Login - http://127.0.0.1:8000/login
    path('accounts/profile/', views.profile_view, name='profile_view'), #Funcion de la pantalla profile - http://localhost:8000/accounts/profile/
    path('accounts/profile/', RedirectView.as_view(url='/'), name='redirect_to_home'),#Funcion retroceso de pantalla
    path('logout/', views.logout, name='logout_custom'),
    path('logout2/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),#Al darle salir redirige a la pantalla de login
    path('social-auth/', include('social_django.urls', namespace='social')),  # Añade 

    #Modulos 
    path('', include('Seguridad.urls')),
    path('', include('Gestion_Contenido.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)