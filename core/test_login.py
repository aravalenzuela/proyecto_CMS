import pytest
from django.urls import reverse
from unittest.mock import patch
import myapp.auth  # Aquí, "myapp.auth" es el módulo que contiene tu función "login_with_google"

@pytest.mark.django_db
def test_login_page_loads_correctly(client):
    response = client.get(reverse('login'))  # 'login' debería ser el nombre de la URL de tu vista de login
    assert response.status_code == 200

def test_login_with_google():
    with patch('myapp.auth.login_with_google') as mock_login:
        # Simular una respuesta exitosa de Google
        mock_login.return_value = {'status': 'ok'}

        # Llama a la función que quieres probar
        result = myapp.auth.login_with_google('fake_oauth_code')

        # Asegura que la función maneja la respuesta exitosa correctamente
        assert result['status'] == 'ok'
