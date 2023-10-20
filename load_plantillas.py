# En tu script load_plantillas.py
from Gestion_Contenido.models import Plantilla

# Crear instancias de plantillas
plantilla20 = Plantilla(nombre="Plantilla 20", tipo="multimedia", contenido="Contenido de la plantilla 20")
plantilla20.save()
plantilla21 = Plantilla(nombre="Plantilla 21", tipo="blog", contenido="Contenido de la plantilla 21")
plantilla21.save()



# Agrega más plantillas si es necesario
