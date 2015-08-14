"""Production settings and globals."""

import yaml


from os import environ

from os.path import dirname, join
from common import *


########## JSON CONFIGURATION


SERVICE_NAME = 'django'
CONFIG_ROOT = environ.get('CONFIG_ROOT', dirname(SITE_ROOT))

with open(join(CONFIG_ROOT, SERVICE_NAME) + ".auth.yaml") as auth_file:
    AUTH_TOKENS = yaml.load(auth_file)

with open(join(CONFIG_ROOT, SERVICE_NAME) + ".env.yaml") as env_file:
    ENV_TOKENS = yaml.load(env_file)
########## END JSON CONFIGURATION

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = ENV_TOKENS.get('EMAIL_HOST', None)
EMAIL_PORT = ENV_TOKENS.get('EMAIL_PORT', 587)
EMAIL_HOST_PASSWORD = AUTH_TOKENS.get('EMAIL_HOST_PASSWORD', None)
EMAIL_HOST_USER = AUTH_TOKENS.get('EMAIL_HOST_USER', None)

EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME
EMAIL_USE_TLS = True

SERVER_EMAIL = ENV_TOKENS.get('SERVER_EMAIL', 'counter@edunext.co')
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION

DATABASES = AUTH_TOKENS['DATABASES']

########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION

CACHES = AUTH_TOKENS['CACHES']

########## END CACHE CONFIGURATION


########## CELERY CONFIGURATION

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-transport
# BROKER_TRANSPORT = 'amqplib'

# Set this number to the amount of allowed concurrent connections on your AMQP
# provider, divided by the amount of active workers you have.

# For example, if you have the 'Little Lemur' CloudAMQP plan (their free tier),
# they allow 3 concurrent connections. So if you run a single worker, you'd
# want this number to be 3. If you had 3 workers running, you'd lower this
# number to 1, since 3 workers each maintaining one open connection = 3
# connections total.

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-pool-limit
# BROKER_POOL_LIMIT = 3

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-connection-max-retries
# BROKER_CONNECTION_MAX_RETRIES = 0

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-url
# BROKER_URL = environ.get('RABBITMQ_URL') or environ.get('CLOUDAMQP_URL')   # this should come from the auth.json

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
# CELERY_RESULT_BACKEND = 'amqp'

########## END CELERY CONFIGURATION


########## STORAGE CONFIGURATION
# See: http://django-storages.readthedocs.org/en/latest/index.html
INSTALLED_APPS += (
    'storages',
)

# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
DEFAULT_FILE_STORAGE = AUTH_TOKENS.get('STATICFILES_STORAGE', 'storages.backends.s3boto.S3BotoStorage')

# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
# AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = AUTH_TOKENS.get('AWS_ACCESS_KEY_ID', 'AKIAIF6JLBEGC3WL6CQQ')
AWS_SECRET_ACCESS_KEY = AUTH_TOKENS.get('AWS_SECRET_ACCESS_KEY', '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')
AWS_STORAGE_BUCKET_NAME = AUTH_TOKENS.get('AWS_STORAGE_BUCKET_NAME', 'enext-analytics')
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIREY = 60 * 60 * 24 * 7
AWS_HEADERS = {
    'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (
        AWS_EXPIREY,
        AWS_EXPIREY
    )
}

# Serving the files from S3 causes a No 'Access-Control-Allow-Origin' or problems with require and the /static/ path
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_ROOT = ENV_TOKENS.get('STATIC_ROOT', STATIC_ROOT)

########## END STORAGE CONFIGURATION


########## COMPRESSION CONFIGURATION
# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_STORAGE
COMPRESS_STORAGE = DEFAULT_FILE_STORAGE

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_CSS_FILTERS
COMPRESS_CSS_FILTERS += [
    'compressor.filters.cssmin.CSSMinFilter',
]

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_JS_FILTERS
COMPRESS_JS_FILTERS += [
    'compressor.filters.jsmin.JSMinFilter',
]
########## END COMPRESSION CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = AUTH_TOKENS.get('SECRET_KEY', SECRET_KEY)
########## END SECRET CONFIGURATION


########## DOMAIN CONFIGURATION

ALLOWED_HOSTS = ENV_TOKENS.get('ALLOWED_HOSTS', ['*'])

########## END DOMAIN CONFIGURATION
