import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_login_page_loads_correctly(client):
    response = client.get(reverse('login'))  # 'login' debería ser el nombre de la URL de tu vista de login
    assert response.status_code == 200
