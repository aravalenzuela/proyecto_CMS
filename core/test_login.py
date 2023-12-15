
import pytest
from django.test import SimpleTestCase, RequestFactory, Client
from django.urls import reverse, resolve
from core.views import home,login_view, logout, profile_view
from django.contrib.auth.models import AnonymousUser, User

"""
test para los urls del sistema
"""
class Test_urls(SimpleTestCase):

  def test_home(self):
    url = reverse('home')
    self.assertEqual(resolve(url).func, home, "no se pudo dirigir a el url home")

  def test_login(self):
    url = reverse('login')
    self.assertEqual(resolve(url).func,login_view)

  def test_logout(self):
    url = reverse('logout_custom') #HAce referencia al name de lo que esta en la urls.py
    self.assertEqual(resolve(url).func,logout)

  def test_login2(self):
    url = reverse('login')
    self.assertEqual(resolve(url).func,login_view)

@pytest.mark.django_db
def test_profile_view_authenticated_user(client):
    # Create a user and log them in
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    
    url = reverse('profile')  # Ensure 'profile' matches the actual name in your urls.py

    response = client.get(url)
    
    # Chequea si el status es 200
    assert response.status_code == 200

@pytest.mark.django_db
def test_panel_autor_view():
    client = Client()
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('panel_autor')
    response = client.get(url)
    assert response.status_code == 200
    assert 'panel_autor.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_panel_editores_view():
    client = Client()
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('panel_editores')
    response = client.get(url)
    assert response.status_code == 200
    assert 'panel_editores.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_panel_publicador_view():
    client = Client()
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('panel_publicador')
    response = client.get(url)
    assert response.status_code == 200
    assert 'panel_publicador.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_panel_suscriptor_view():
    client = Client()
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    url = reverse('panel_suscriptor')
    response = client.get(url)
    assert response.status_code == 200
    assert 'panel_suscriptor.html' in [t.name for t in response.templates]