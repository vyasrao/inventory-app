import os
import sqlalchemy
from sqlalchemy.orm import scoped_session

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w(4#5(88-o+gt2kwhu@bn!f69i$g2zvmc#$a9f-uc#^0z%o8+u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


DB_HOST = 'localhost'
DBMS = 'mysql+mysqlconnector'
DB_PORT = ''
DB_NAME = 'ims_2'
DB_USER = 'root'
DB_PWD = 'dbvyas'

DB_ENGINE_URL = '%s://%s:%s@%s/%s' % (DBMS, DB_USER, DB_PWD, DB_HOST,DB_NAME)

engine = sqlalchemy.create_engine(DB_ENGINE_URL, echo=False)

#engine = sqlalchemy.create_engine('sqlite:///loose.sqlite', connect_args={'check_same_thread': False}, echo=True)
#engine = sqlalchemy.create_engine('mysql+mysqldb://vyas:vyas@localhost/IMS', connect_args={'check_same_thread': False}, echo=True)

Session = scoped_session(sqlalchemy.orm.sessionmaker(bind=engine))

# Application definition

INSTALLED_APPS = [
    'inventory.apps.InventoryConfig',
    #'django.contrib.admin',
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    #'django.middleware.security.SecurityMiddleware',
    #'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'weavedin.middleware.DataAccessLayer.DataAccessLayer'
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'weavedin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), '../templates').replace('\\','/')],
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

WSGI_APPLICATION = 'weavedin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

#AUTH_PASSWORD_VALIDATORS = [
#    {
#        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#    },
#    {
#        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#    },
#    {
#        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#    },
#    {
#        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#    },
#]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

#STATIC_URL = '/static/'

STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = ( os.path.join('static'), )