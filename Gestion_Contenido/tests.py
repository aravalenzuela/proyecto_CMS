from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from .models import Plantilla

class ListarPlantillasTest(TestCase):
    def test_listar_plantillas(self):
        # Crea algunas plantillas de ejemplo en la base de datos
        Plantilla.objects.create(nombre='Plantilla 1', tipo='Tipo 1')
        Plantilla.objects.create(nombre='Plantilla 2', tipo='Tipo 2')

        # Accede a la vista 'listar_plantillas' a través de su URL
        url = reverse('listar_plantillas')  
        response = self.client.get(url)

        # Verifica si la página se carga correctamente
        self.assertEqual(response.status_code, 200)

        # Verifica si las plantillas se muestran en la respuesta
        self.assertContains(response, 'Plantilla 1')
        self.assertContains(response, 'Plantilla 2')


class SeleccionarPlantillaTest(TestCase):
    def test_seleccionar_plantilla(self):
        # Tenemos una vista llamada 'seleccionar_plantilla'
        # Escribir pruebas para esta vista aquí
        # Asegurar  que esta vista funcione correctamente para seleccionar plantillas
        #  que los datos se guarden correctamente en la base de datos
        pass  # Reemplazar esto con el código de prueba

