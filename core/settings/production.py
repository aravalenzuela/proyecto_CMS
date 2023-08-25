
from core.settings.base import *

import dj_database_url
from decouple import config

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://dbdesarrollo_user:1O7bRJuKl9Entwp4487p6995DwLbmAG0@dpg-cjkal8ephtvs73cop1o0-a.oregon-postgres.render.com/dbdesarrollo'
    )
}

CSRF_TRUSTED_ORIGINS = ['https://cms-is2.onrender.com/']