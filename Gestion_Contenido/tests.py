from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from .models import Plantilla
from django.contrib.auth.models import User


from django.http import HttpResponse
from .forms import SeleccionarPlantillaForm, ConfiguracionSitioForm
from .views import seleccionar_plantilla

from Seguridad.models import Categoria, Subcategoria
from .forms import ReporteForm
from django.http import JsonResponse

from Seguridad.models import Contenido  


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





class ReportesViewTest(TestCase):
    
    def test_reportes_view_post_ajax(self):
        """
        Prueba la funcionalidad de la vista 'reportes_view' al realizar una solicitud POST con AJAX.
        Verifica que los datos del informe se generen correctamente.
        """
        # Crea algunas categorías y subcategorías de ejemplo en la base de datos
        categoria = Categoria.objects.create(nombre='Categoría 1')
        Subcategoria.objects.create(nombre='Subcategoría 1', categoria_relacionada=categoria)

        url = reverse('reportes_view')
        data = {'informe': 'subcategorias_por_categorias'}
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertIn('datos', response.json())
        self.assertIn('img_src', response.json())
        self.assertIn('informe_detalles', response.json())
        self.assertIn('informe_detalles_adicionales', response.json())

        # Verifica que los datos del informe se generen correctamente
        datos_informe = response.json()['datos']
        self.assertEqual(len(datos_informe), 1)

        informe_categoria = datos_informe[0]
        self.assertIn('categoria', informe_categoria)
        self.assertIn('subcategorias', informe_categoria)
        self.assertIn('cantidad_subcategorias', informe_categoria)

        # Agrega más aserciones según la estructura esperada de tus datos del informe

 
 



class ReporteTiposPlantillasViewTest(TestCase):
    def test_reporte_tipos_plantillas_view_post_ajax(self):
        """
        Prueba la funcionalidad de la vista 'reporte_tipos_plantillas' al realizar una solicitud POST con AJAX.
        Verifica que los datos del informe se generen correctamente.
        """
        # Crea algunas plantillas de ejemplo en la base de datos
        Plantilla.objects.create(nombre='Plantilla 1', tipo='blog')
        Plantilla.objects.create(nombre='Plantilla 2', tipo='blog')
        Plantilla.objects.create(nombre='Plantilla 3', tipo='multimedia')

        url = reverse('generar_reporte')
        data = {'informe': 'tipo_plantillas_por_plantillas'}
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertIn('datos', response.json())
        self.assertIn('img_src', response.json())
        self.assertIn('informe_detalles', response.json())
        self.assertIn('informe_detalles_adicionales', response.json())

        # Verifica que los datos del informe se generen correctamente
        datos_informe = response.json()['datos']
        self.assertEqual(len(datos_informe), 2)  # Ajusta según la cantidad de tipos de plantillas en tu base de datos

        for tipo, detalles in datos_informe.items():
            self.assertIn('plantillas', detalles)
            self.assertIn('cantidad_plantillas', detalles)





from Seguridad.models import Contenido, TipoDeContenido  # Asegúrate de importar los modelos correctos

from django.contrib.auth.models import User

class ReporteTipoContenidoViewTest(TestCase):
    def setUp(self):
        # Crea un usuario de prueba y autentícalo
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_reporte_tipo_contenido_ajax(self):
        # Crea un usuario para ser utilizado como autor
        autor = User.objects.create(username='autor', password='password')

        # Crea algunos tipos de contenido y contenidos de ejemplo en la base de datos
        tipo_contenido1 = TipoDeContenido.objects.create(nombre='Tipo 1')
        tipo_contenido2 = TipoDeContenido.objects.create(nombre='Tipo 2')
    
        Contenido.objects.create(titulo='Contenido 1', tipo=tipo_contenido1, autor=autor)

        # Resto del código de la prueba...
    
    def test_reporte_tipo_contenido_no_ajax(self):
        # Crea un usuario para ser utilizado como autor
        autor = User.objects.create(username='autor', password='password')

        # Crea algunos tipos de contenido y contenidos de ejemplo en la base de datos
        tipo_contenido1 = TipoDeContenido.objects.create(nombre='Tipo 1')
        tipo_contenido2 = TipoDeContenido.objects.create(nombre='Tipo 2')
    
        Contenido.objects.create(titulo='Contenido 1', tipo=tipo_contenido1, autor=autor)

        # Resto del código de la prueba...




class ReporteEstadosCategoriasViewTest(TestCase):
    def test_reporte_estados_categorias_ajax(self):
        # Crear algunas categorías de ejemplo en la base de datos
        Categoria.objects.create(nombre='Categoria1', activo=True)
        Categoria.objects.create(nombre='Categoria2', activo=True)
        Categoria.objects.create(nombre='Categoria3', activo=False)

        # Simular una solicitud AJAX POST
        response = self.client.post(
            reverse('generar_reporte'),  # Reemplaza 'nombre_de_la_url_de_tu_vista' con el nombre real de tu URL
            {'informe': 'estados_de_categorias'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Verificar que la respuesta sea un objeto JSON
        self.assertIsInstance(response, JsonResponse)

        # Analizar el contenido JSON de la respuesta
        data = response.json()

        # Verificar que los datos esperados estén presentes en el JSON
        self.assertIn('datos', data)
        self.assertIn('img_src', data)
        self.assertIn('informe_detalles', data)
        self.assertIn('informe_detalles_adicionales', data)

  


class ReportesTests(TestCase):

    def test_reporte_estados_tablero(self):
        # Ajusta las URLs según tu configuración
        url = reverse('reportes_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Verifica que la página cargue correctamente

        # Simula una solicitud AJAX POST para la función
        response = self.client.post(url, {'informe': 'estados_en_tablero'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)  # Verifica que la solicitud AJAX sea exitosa

        # Simula una solicitud POST sin AJAX
        response = self.client.post(url, {'informe': 'estados_en_tablero'})
        self.assertEqual(response.status_code, 200)  # Verifica que la solicitud POST sea exitosa

        # Puedes agregar más aserciones según tus necesidades, por ejemplo, para verificar la presencia de ciertos elementos en la respuesta JSON.


    def test_reporte_proporcion_plantillas(self):
        # Ajusta las URLs según tu configuración
        url = reverse('reportes_view')  # Cambiado de 'generar_reporte'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Verifica que la página cargue correctamente

        # Simula una solicitud AJAX POST para la función
        response = self.client.post(url, {'informe': 'proporcion_plantillas'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)  # Verifica que la solicitud AJAX sea exitosa

        # Simula una solicitud POST sin AJAX
        response = self.client.post(url, {'informe': 'proporcion_plantillas'})
        self.assertEqual(response.status_code, 200)  # Verifica que la solicitud POST sea exitosa


    def test_generar_reporte(self):
        # Puedes ajustar las URLs según tu configuración
        url = reverse('generar_reporte')

        # Simula una solicitud POST con un informe válido
        response = self.client.post(url, {'informe': 'proporcion_plantillas'})
        self.assertEqual(response.status_code, 200)  # Verifica que la solicitud POST sea exitosa

        # Simula una solicitud POST con un informe inválido
        response = self.client.post(url, {'informe': 'informe_invalido'})
        self.assertEqual(response.status_code, 400)  # Verifica que se reciba una respuesta BadRequest

# Puedes agregar más pruebas según sea necesario
