# En tu script load_plantillas.py
from Gestion_Contenido.models import Plantilla

# Crear instancias de plantillas
plantilla300 = Plantilla(nombre="Plantilla 300", tipo="blog", contenidoDePlantilla="Contenido de la plantilla 300")
plantilla300.save()
plantilla301 = Plantilla(nombre="Plantilla 301", tipo="multimedia", contenidoDePlantilla="Contenido de la plantilla 301")
plantilla301.save()



# Agrega más plantillas si es necesario
