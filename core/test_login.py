
import pytest
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import home,login_view
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

       