# En tu script load_plantillas.py
from Gestion_Contenido.models import Plantilla

# Crear instancias de plantillas
plantilla7 = Plantilla(nombre="Plantilla 7", tipo="blog", contenido="Contenido de la plantilla 7", predeterminada=True)
plantilla7.save()
plantilla8 = Plantilla(nombre="Plantilla 8", tipo="multimedia", contenido="Contenido de la plantilla 8", predeterminada=True)
plantilla8.save()



# Agrega más plantillas si es necesario
