import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-&n_=i3(5*6i2z3i81nn1nch*3!@b@z%3t060@1qmx9gq%t4y2f')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['sgrdv-orl.onrender.com', '127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'comptes',
    'patients',
    'medecins',
    'rdv',
    'paiements',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SGRDV_ORL.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'rdv.context_processors.notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'SGRDV_ORL.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Brazzaville'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration d'authentification
LOGIN_URL = 'comptes:login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

JAZZMIN_SETTINGS = {
    # Titres du site
    "site_title": "BERNADETTE Admin",
    "site_header": "BERNADETTE",
    "site_brand": "BERNADETTE ORL",
    "welcome_sign": "Bienvenue sur le panel d'administration BERNADETTE",
    "copyright": "BERNADETTE - Assistante Sanitaire ORL",
    "search_model": ["patients.Patient", "rdv.RendezVous"],

    # Liens du menu du haut
    "topmenu_links": [
        {"name": "Accueil du Site", "url": "comptes:index", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
    ],

    # Configuration des icônes de vos applications (FontAwesome)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user-lock",
        "patients.patient": "fas fa-user-injured",
        "medecins.medecin": "fas fa-user-md",
        "rdv.rendezvous": "fas fa-calendar-check",
        "paiements.paiement": "fas fa-credit-card",
    },
    
    # Organisation visuelle
    "navigation_expanded": True,
    "order_with_respect_to": ["patients", "medecins", "rdv", "paiements", "auth"],
}

# CONFIGURATION DU THÈME (Les couleurs vert médical de votre template)
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    
    # Couleur du bandeau supérieur (Couleur sombre de votre navbar)
    "navbar": "navbar-teal", 
    "theme": "cerulean", # Base moderne
    "sidebar": "sidebar-dark-teal", # Couleur de fond du menu latéral
    
    # Style des boutons et éléments actifs (Le vert vif de PrimeDental)
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    
    # Couleur d'accentuation pour les boutons "Enregistrer" et les liens
    "accent": "accent-teal",
    "button_classes": {
        "primary": "btn-teal",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# Utilisation du gestionnaire d'e-mails natif de Django
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# 1. Le serveur (Texte)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')

# 2. Le port : PIÈGE ! Il faut obligatoirement le convertir en entier (int)
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))

# 3. Le TLS : PIÈGE ! Render renvoie le texte "True", Django exige un booléen True
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'

# 4. Vos identifiants
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'donimatsiona@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'dxpb ocjz eqzh aazf')

# 5. Les variables pour vos vues
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', EMAIL_HOST_USER)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
