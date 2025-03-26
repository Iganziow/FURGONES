import os
from pathlib import Path

# Construir rutas base
BASE_DIR = Path(__file__).resolve().parent.parent
AUTH_USER_MODEL = 'furgones.Conductor'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # ✅ Backend estándar de autenticación
]

# Configurar una clave secreta para uso local (reemplázala si quieres)
SECRET_KEY = "django-insecure-local-key"

# Modo debug activado solo para desarrollo local
DEBUG = False

# Permitir que solo el localhost acceda a la app
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Configuración de base de datos SQLite para local
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Archivos estáticos
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Configuración de apps instaladas y middlewares (sin cambios grandes)
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "furgones",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Carpeta donde estarán las plantillas
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

LOGIN_URL = 'login'  # Nombre de la ruta o URL para la pantalla de login
LOGIN_REDIRECT_URL = 'redireccion_dashboard'  # Nombre de la ruta que definiste
LOGOUT_REDIRECT_URL = 'login'  # A dónde ir al hacer logout

# Configuración de URLs y WSGI
ROOT_URLCONF = "Enruta.urls"
WSGI_APPLICATION = "Enruta.wsgi.application"

# Configuración de internacionalización
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# Archivos estáticos y media
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
