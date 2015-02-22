#  ____ _____ ___  ____  _
# / ___|_   _/ _ \|  _ \| |
# \___ \ | || | | | |_) | |
#  ___) || || |_| |  __/|_|
# |____/ |_| \___/|_|   (_)
#
# Do not edit this file when installing RatticDB. This file read in the
# settings from INI style files in conf/local.cfg and /etc/ratticweb.cfg.
# You should make you changes to those files.
#
# If you believe changes are required to these files please write your code
# to pull the values from these config files (see the code already here)
# and then submit a Pull Request to us on GitHub.
#
# GitHub: https://github.com/tildaslash/RatticWeb
#
from ConfigParser import RawConfigParser, NoOptionError
from urlparse import urljoin
import ldap
import os
from django_auth_ldap.config import LDAPSearch
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _

config = RawConfigParser()
config.readfp(open('conf/defaults.cfg'))
CONFIGURED_BY = config.read(['conf/local.cfg', '/etc/ratticweb.cfg'])


def confget(section, var, default):
    try:
        return config.get(section, var)
    except NoOptionError:
        return default


def confgetbool(section, var, default):
    try:
        return config.getboolean(section, var)
    except NoOptionError:
        return default

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# The Internationalization Settings
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = (
    'conf/locale',
)
LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('de', _('German')),
)

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# A tuple of callables that are used to populate the context in
# RequestContext. These callables take a request object as their
# argument and return a dictionary of items to be merged into
# the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'ratticweb.context_processors.base_template_reqs',
    'ratticweb.context_processors.logo_selector',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',

    # Custom Middleware
    'account.middleware.StrictAuthentication',
    'account.middleware.PasswordExpirer',
    'ratticweb.middleware.DisableClientSideCachingMiddleware',
    'ratticweb.middleware.XUACompatibleMiddleware',
    'ratticweb.middleware.CSPMiddleware',
    'ratticweb.middleware.HSTSMiddleware',
    'ratticweb.middleware.DisableContentTypeSniffing',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ratticweb.urls'

# Urls
RATTIC_ROOT_URL = config.get('ratticweb', 'urlroot')
MEDIA_URL = urljoin(RATTIC_ROOT_URL, 'media/')
STATIC_URL = urljoin(RATTIC_ROOT_URL, 'static/')

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ratticweb.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

LOCAL_APPS = (
    # Sub apps
    'ratticweb',
    'cred',
    'account',
    'staff',
    'help',
)

INSTALLED_APPS = (
    # External apps
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'user_sessions',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'south',
    'tastypie',
    'kombu.transport.django',
    'djcelery',
    'database_files',
    'social_auth',
) + LOCAL_APPS

if os.environ.get("ENABLE_TESTS") == "1":
    INSTALLED_APPS += ('django_nose', )

TEST_RUNNER = 'tests.runner.ExcludeAppsTestSuiteRunner'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_format': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console_format'
        }
    },
    'loggers': {
        'django_auth_ldap': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': True,
        },
        'db_backup': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

#######################
# Custom app settings #
#######################

# URLs
PUBLIC_HELP_WIKI_BASE = 'https://github.com/tildaslash/RatticWeb/wiki/'
LOGIN_REDIRECT_URL = urljoin(RATTIC_ROOT_URL, "cred/list/")
LOGIN_URL = RATTIC_ROOT_URL

# django-user-sessions
SESSION_ENGINE = 'user_sessions.backends.db'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Icon configuration
CRED_ICON_JSON = 'db/icons.json'
CRED_ICON_CSS = 'ratticweb/static/rattic/css/icons.css'
CRED_ICON_SPRITE = 'rattic/img/sprite.png'
CRED_ICON_BASEDIR = 'rattic/img/credicons'
CRED_ICON_CLEAR = 'rattic/img/clear.gif'
CRED_ICON_DEFAULT = 'Key.png'

# django-auth-ldap
AUTH_LDAP_USER_ATTR_MAP = {"email": "mail", }
AUTH_LDAP_USER_FLAGS_BY_GROUP = {}
AUTH_LDAP_MIRROR_GROUPS=True

# celery
BROKER_URL = 'django://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'

###############################
# External environment config #
###############################

# [ratticweb]
DEBUG = confgetbool('ratticweb', 'debug', False)
TEMPLATE_DEBUG = DEBUG
TIME_ZONE = config.get('ratticweb', 'timezone')
SECRET_KEY = config.get('ratticweb', 'secretkey')
ALLOWED_HOSTS = [config.get('ratticweb', 'hostname'), 'localhost']
HOSTNAME = config.get('ratticweb', 'hostname')
RATTIC_MAX_ATTACHMENT_SIZE = int(config.get('ratticweb', 'max_attachment_size'))
RATTIC_DISABLE_EXPORT = config.getboolean('ratticweb', 'disable_export')

# Allow SSL termination outside RatticDB
if confget('ratticweb', 'ssl_header', False):
    SECURE_PROXY_SSL_HEADER = (config.get('ratticweb', 'ssl_header'), config.get('ratticweb', 'ssl_header_value'))

# Setup the loglevel
LOGGING['loggers']['django.request']['level'] = config.get('ratticweb', 'loglevel')

# [filepaths]
HELP_SYSTEM_FILES = confget('filepaths', 'help', False)
MEDIA_ROOT = confget('filepaths', 'media', '')
STATIC_ROOT = confget('filepaths', 'static', '')

# [database]
DATABASES = {
    'default': {
        'ENGINE': confget('database', 'engine', 'django.db.backends.sqlite3'),
        'NAME': confget('database', 'name', 'db/ratticweb'),
        'USER': confget('database', 'user', ''),
        'PASSWORD': confget('database', 'password', ''),
        'HOST': confget('database', 'host', ''),
        'PORT': confget('database', 'port', ''),
    }
}

# [backup]
BACKUP_DIR = confget("backup", "dir", None)
BACKUP_GPG_HOME = confget("backup", "gpg_home", None)
BACKUP_S3_BUCKET = confget("backup", "s3_bucket", None)
BACKUP_RECIPIENTS = confget("backup", "recipients", None)

# [email]
# SMTP Mail Opts
EMAIL_BACKEND = config.get('email', 'backend')
EMAIL_FILE_PATH = config.get('email', 'filepath')
EMAIL_HOST = config.get('email', 'host')
EMAIL_PORT = config.get('email', 'port')
EMAIL_HOST_USER = config.get('email', 'user')
EMAIL_HOST_PASSWORD = config.get('email', 'password')
EMAIL_USE_TLS = confgetbool('email', 'usetls', False)
DEFAULT_FROM_EMAIL = config.get('email', 'from_email')

# [scheduler]
CELERYBEAT_SCHEDULE = {}

chgqreminder = int(config.get('scheduler', 'change_queue_reminder_period'))
if chgqreminder > 0:
    CELERYBEAT_SCHEDULE['send-change-queue-reminder-email'] = {
        'task': 'cred.tasks.change_queue_emails',
        'schedule': timedelta(days=chgqreminder),
    }

CELERY_TIMEZONE = TIME_ZONE

# [ldap]
LDAP_ENABLED = 'ldap' in config.sections()

if LDAP_ENABLED:
    # Add LDAP to the auth modules
    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    # Setup the LDAP Logging
    LOGGING['loggers']['django_auth_ldap']['level'] = confget('ldap', 'loglevel', 'WARNING')

    # Get config options for LDAP
    AUTH_LDAP_SERVER_URI = config.get('ldap', 'uri')
    AUTH_LDAP_BIND_DN = confget('ldap', 'binddn', '')
    AUTH_LDAP_BIND_PASSWORD = confget('ldap', 'bindpw', '')

    if config.has_option('ldap', 'staff'):
        AUTH_LDAP_USER_FLAGS_BY_GROUP['is_staff'] = config.get('ldap', 'staff')

    # Searching for things
    AUTH_LDAP_USER_SEARCH = LDAPSearch(config.get('ldap', 'userbase'), ldap.SCOPE_SUBTREE, config.get('ldap', 'userfilter'))

    # Groups lookup and mirroring
    if config.has_option('ldap', 'groupfilter'):
        AUTH_LDAP_GROUP_SEARCH = LDAPSearch(config.get('ldap', 'groupbase'), ldap.SCOPE_SUBTREE, config.get('ldap', 'groupfilter'))
        AUTH_LDAP_GROUP_TYPE = getattr(__import__('django_auth_ldap').config, config.get('ldap', 'grouptype'))()
    else:
        AUTH_LDAP_MIRROR_GROUPS = False

    # Booleans
    AUTH_LDAP_ALLOW_PASSWORD_CHANGE = confgetbool('ldap', 'pwchange', False)
    AUTH_LDAP_START_TLS = confgetbool('ldap', 'starttls', False)
    AUTH_LDAP_GLOBAL_OPTIONS = {
        ldap.OPT_X_TLS_REQUIRE_CERT: confgetbool('ldap', 'requirecert', True),
        ldap.OPT_REFERRALS: confgetbool('ldap', 'referrals', False),
    }

# [goauth2]
GOAUTH2_ENABLED = 'goauth2' in config.sections()

if GOAUTH2_ENABLED:
    AUTHENTICATION_BACKENDS = (
        'social_auth.backends.google.GoogleOAuth2Backend',
        'django.contrib.auth.backends.ModelBackend',
    )

    LOGIN_URL = RATTIC_ROOT_URL + 'account/login/google-oauth2/'
    LOGIN_REDIRECT_URL = urljoin(RATTIC_ROOT_URL, 'account/autocreateusergroup')
    LOGIN_ERROR_URL = RATTIC_ROOT_URL + '/account/login-error/'

    SOCIAL_AUTH_RAISE_EXCEPTIONS = False
    SOCIAL_AUTH_PROCESS_EXCEPTIONS = 'social_auth.utils.log_exceptions_to_messages'

    GOOGLE_OAUTH2_CLIENT_ID = config.get('goauth2', 'client_id')
    GOOGLE_OAUTH2_CLIENT_SECRET = config.get('goauth2', 'client_secret')
    GOOGLE_WHITE_LISTED_DOMAINS = [config.get('goauth2', 'domain')]

    SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
    SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
    SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

    if confgetbool('goauth2', 'https_redirect', False):
        SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

    SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]

    SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

# Passwords expiry settings
if GOAUTH2_ENABLED:
    PASSWORD_EXPIRY = False
else:
    try:
        PASSWORD_EXPIRY = timedelta(days=int(config.get('ratticweb', 'passwordexpirydays')))
    except NoOptionError:
        PASSWORD_EXPIRY = False
    except ValueError:
        PASSWORD_EXPIRY = False
