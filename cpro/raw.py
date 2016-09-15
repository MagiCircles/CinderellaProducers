from django.utils.translation import ugettext_lazy as _

ACCOUNT_TABS = [
    ('Cards', _('Cards'), 'album'),
    ('About', _('About'), 'about'),
    ('Events', _('Events'), 'event'),
    ('Songs', _('Songs'), 'song'),
]
ACCOUNT_TABS_LIST = [name for (name, _, _) in ACCOUNT_TABS]
