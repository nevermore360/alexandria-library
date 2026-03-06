from .development import *  # noqa: F401, F403

DEBUG = False

# HTTPS is terminated by the outer nginx-proxy; Django receives HTTP internally
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False

# Cookies must be secure now that HTTPS is in place
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Required by Django 4.0+ for CSRF validation when behind an HTTPS proxy
CSRF_TRUSTED_ORIGINS = ['https://app.bxm-group.com']

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO'},
}
