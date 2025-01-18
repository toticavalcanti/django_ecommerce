import os
import environ
import logging

# Definindo o logger
logger = logging.getLogger(__name__)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Setup environment variables
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
print(f"ALLOWED_HOSTS: {env.list('ALLOWED_HOSTS', default=[])}")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'xjmv-0^l__duq4-xp54m94bsf02lx4&1xka_ykd_(7(5#9^1o^'
SECRET_KEY = env('SECRET_KEY', default='xjmv-0^l__duq4-xp54m94bsf02lx4&1xka_ykd_(7(5#9^1o^')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Stripe Configuration
STRIPE_API_KEY = env('STRIPE_API_KEY')
STRIPE_PUB_KEY = env('STRIPE_PUB_KEY')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # our apps
    'addresses',
    'analytics',
    'billing',
    'accounts',
    'carts',
    'orders',
    'products',
    'search',
    'tags',
    'categories',
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Define o modelo de usuário customizado
AUTH_USER_MODEL = 'accounts.User'

# Configurações adicionais para controle de sessão
FORCE_SESSION_TO_ONE = False  # Permite múltiplas sessões para o mesmo usuário
FORCE_INACTIVE_USER_ENDSESSION = False  # Não encerra a sessão de usuários inativos automaticamente

# Configuração de sessão para o frontend
SESSION_COOKIE_NAME = 'frontend_sessionid'  # Nome do cookie para sessões do frontend
SESSION_COOKIE_AGE = 1209600  # Duração padrão de 2 semanas (14 dias)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Não expira ao fechar o navegador
SESSION_COOKIE_PATH = '/'  # Define o escopo do cookie para toda a aplicação

# Configuração de sessão para o admin
ADMIN_SESSION_COOKIE_NAME = 'admin_sessionid'  # Nome do cookie para sessões do admin
ADMIN_SESSION_COOKIE_AGE = 3600  # Duração de 1 hora para sessões do admin

# Configurações de segurança para os cookies
SESSION_COOKIE_SECURE = False  # Use True em produção (requer HTTPS)
SESSION_COOKIE_HTTPONLY = True  # Impede acesso via JavaScript
SESSION_COOKIE_SAMESITE = 'Lax'  # Melhora a segurança contra CSRF'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'e_commerce.session_middleware.SeparateAdminSessionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGOUT_REDIRECT_URL = '/login/'
ROOT_URLCONF = 'e_commerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'e_commerce.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_local")
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "static_root")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media_root")

logger.info(f"Static files directory: {STATIC_ROOT}")
logger.info(f"Media files directory: {MEDIA_ROOT}")

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}