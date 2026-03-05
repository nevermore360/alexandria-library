from .development import *

DEBUG = False

SECURE_SSL_REDIRECT = False  # nginx handles SSL termination; no cert configured
SESSION_COOKIE_SECURE = False  # no HTTPS; Secure flag would block cookies over HTTP
CSRF_COOKIE_SECURE = False    # no HTTPS; Secure flag would block cookies over HTTP
SECURE_HSTS_SECONDS = 0       # disabled: HSTS + no HTTPS locks browsers out of the site
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO'},
}