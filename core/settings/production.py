
from core.settings.base import *

import dj_database_url
from decouple import config

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://bd_proyecto_cms_is2_user:SyG6Zn5uyiHIZ8MHN9tQs9UJxr8lZkYg@dpg-ck0g7ve3ktkc73e4eukg-a.oregon-postgres.render.com/bd_proyecto_cms_is2'
    )
}

CSRF_TRUSTED_ORIGINS = ['https://cms-is2.onrender.com']

# Static  files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEBUG = True

