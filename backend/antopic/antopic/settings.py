import datetime
import os
from dotenv import load_dotenv
import ssl
load_dotenv()

DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
API_AUDIENCE = os.environ['API_AUDIENCE']
ALLOWED_HOSTS = ['http://localhost:8080', "http://10.0.0.176:8080", "*"]

ROOT_URLCONF = 'antopic.urls'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']
BROKER_USE_SSL = {'ssl_cert_reqs': ssl.CERT_NONE}
CELERY_REDIS_BACKEND_USE_SSL = {'ssl_cert_reqs': ssl.CERT_NONE}


SIMPLE_JWT = {
    'ALGORITHM': 'RS256',
    'AUDIENCE': API_AUDIENCE,
    'ISSUER': f"https://{AUTH0_DOMAIN}/",
    'JWK_URL': f"https://{AUTH0_DOMAIN}/.well-known/jwks.json",
    "USER_ID_CLAIM": f"{API_AUDIENCE}/email",
    'JTI_CLAIM': None,
    'TOKEN_TYPE_CLAIM': None,
    'USER_ID_FIELD': 'sub',
    'USER_ID_CLAIM': 'sub',
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    # Custom apps
    'antopic',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthenticatio',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'CLIENT': {
            'name': os.environ['MONGO_DB_NAME'],
            'host': os.environ['MONGO_DB_HOST'],
            'authMechanism': 'SCRAM-SHA-1',
        }
    }
}

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'antopic.middleware.JWTMiddleware',
]
APPEND_SLASH = False

CORS_ALLOWED_ORIGINS = [
    "https://domain.com",
    "https://api.domain.com",
    "http://localhost:8080",
    "http://127.0.0.1:9000"
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.abspath(__file__), 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
