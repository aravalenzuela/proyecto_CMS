
from core.settings.base import *

import dj_database_url
from decouple import config

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://bd_bk_proyecto_cms_is2_user:CRPeU5wtxwfXbzg4R1YglSPgDcP0OnkD@dpg-clt1mbqpmc4c73dv3gkg-a.oregon-postgres.render.com/bd_bk_proyecto_cms_is2'
    )
}

CSRF_TRUSTED_ORIGINS = ['https://desarrollo-cms-is2-4omt.onrender.com']

# Static  files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEBUG = True

