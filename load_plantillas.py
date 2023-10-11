# En tu script load_plantillas.py
from Gestion_Contenido.models import Plantilla

# Crear instancias de plantillas
plantilla4 = Plantilla(nombre="Plantilla 4", tipo="blog", contenido="Contenido de la plantilla 4", predeterminada=True)
plantilla4.save()



# Agrega más plantillas si es necesario
