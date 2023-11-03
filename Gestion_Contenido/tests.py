from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from .models import Plantilla
from django.contrib.auth.models import User


from django.http import HttpResponse
from .forms import SeleccionarPlantillaForm, ConfiguracionSitioForm
from .views import seleccionar_plantilla


class ListarPlantillasTest(TestCase):
    def test_listar_plantillas(self):

        """
        Prueba la funcionalidad de la vista 'listar_plantillas'.

        Resultados:
        Se crean algunas plantillas de ejemplo en la base de datos, luego se accede a la vista 'listar_plantillas' a través de su URL y se verifica que la página se carga correctamente. Se verifica también que las plantillas se muestran en la respuesta.
        """
                
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
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')


    def test_seleccionar_plantilla_get(self):
        """
        Prueba la funcionalidad de la vista 'seleccionar_plantilla' al realizar una solicitud GET.

        Resultados:
        Se simula una solicitud GET a la vista 'seleccionar_plantilla' y se verifica que la respuesta sea un código de estado HTTP 200. Se verifica también que el formulario y el formulario de configuración estén presentes en la respuesta.
        """
                
        # Simular una solicitud GET
        response = self.client.get(reverse('seleccionar_plantilla'))

        # Verificar que la respuesta sea un código de estado HTTP 200
        self.assertEqual(response.status_code, 200)

        # Verificar que el formulario y el formulario de configuración estén presentes en la respuesta
        self.assertIsInstance(response.context['form'], SeleccionarPlantillaForm)
        self.assertIsInstance(response.context['configuracion_form'], ConfiguracionSitioForm)

    # Agrega más pruebas según sea necesario




