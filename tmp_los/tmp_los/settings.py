from django.conf import settings as django_settings
from tmp_los import models

# Configure and personalize your website here.

SITE_NAME = 'Sample Website'
SITE_URL = 'http://tmp_los.com/'
SITE_IMAGE = 'tmp_los.png'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.tmp_los.com/'
GAME_NAME = 'Sample Game'
DISQUS_SHORTNAME = 'tmp_los'
ACCOUNT_MODEL = models.Account
COLOR = '#4a86e8'
