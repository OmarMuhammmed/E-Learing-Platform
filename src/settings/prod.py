from .base import * 
import os 

DEBUG = False

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.postgresql',
        'NAME' : os.getenv('POSTGRES_DB'),
        'USER' : os.getenv('POSTGRES_USER'),
        'PASSWORD' : os.getenv('POSTGRES_PASSWORD'),
        'HOST' : 'db',
        'PORT' : 5432,
    }
}

REDIS_URL = 'redis://cache:6379'
CACHES['default']['LOCATION'] = REDIS_URL
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [REDIS_URL]

ADMINS = [('Admin', 'amorey2006@gmail.com')]

ALLOWED_HOSTS =  ['*']

# Serve static files using Whitenoise