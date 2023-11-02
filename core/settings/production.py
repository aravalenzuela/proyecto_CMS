
from core.settings.base import *

import dj_database_url
from decouple import config

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://bd_development_proyecto_cms_is2_user:xtZjPMguh4Bix3NnhmqL0hosHP0FKa4N@dpg-ckpep9m2eoec73e1qou0-a/bd_development_proyecto_cms_is2'
    )
}

CSRF_TRUSTED_ORIGINS = ['https://desarrollo-cms-is2-4omt.onrender.com']

# Static  files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEBUG = True

