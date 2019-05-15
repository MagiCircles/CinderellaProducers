# -*- coding: utf-8 -*-
import datetime
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _

ACCOUNT_TABS = [
    ('Cards', _('Cards'), 'album'),
    ('About', _('About'), 'about'),
    ('Events', _('Events'), 'event'),
    ('Songs', _('Songs'), 'song'),
]
ACCOUNT_TABS_LIST = [name for (name, _, _) in ACCOUNT_TABS]


ABOUT = {
    'shortname': 'idolmaster',
    'name': 'IDOLM@STER',
    'd_names': {
        'ja': u'アイドルマスター',
    },
    'image': 'games/icons/idolmaster'
}

LICENSES = OrderedDict([
    ('cinderellagirls', {
        'name': 'Cinderella Girls',
        'd_names': {
            'ja': 'シンデレラガールズ',
        },
        'games': OrderedDict([
            ('deresute', {
                'name': 'Starlight Stage',
                'd_names': {
                    'ja': 'スターライトステージ',
                },
                'image': 'games/appicons/deresute',
                'hashtags': ['デレステ'],
                'release_date': datetime.date(2015, 9, 2),
            }),
        ]),
    }),
    ('millionlive', {
        'name': 'Million Live!',
        'd_names': {
            'ja': 'ミリオンライブ！',
        },
        'games': OrderedDict([
            ('mirishita', {
                'name': ' Theater Days',
                'd_names': {
                    'ja': 'シアターデイズ',
                },
                'image': 'games/appicons/mirishita',
                'hashtags': ['ミリシタ'],
                'redirect': 'https://www.project-imas.com/wiki/THE_iDOLM@STER_Million_Live!:_Theater_Days',
            }),
        ]),
    }),
    ('sidem', {
        'name': 'SideM',
        'd_names': {
            'ja': 'SideM',
        },
        'games': OrderedDict([
            ('emusute', {
                'name': 'LIVE ON ST@GE!',
                'd_names': {
                    'ja': 'LIVE ON ST@GE!',
                },
                'image': 'games/appicons/emusute',
                'hashtags': ['エムステ'],
                'redirect': 'https://www.project-imas.com/wiki/THE_iDOLM@STER_SideM:_LIVE_ON_ST@GE!',
            }),
        ]),
    }),
    ('shinycolors', {
        'name': 'Shiny Colors',
        'd_names': {
            'ja': 'シャイニーカラーズ',
        },
        'games': OrderedDict([
            ('shanimasu', {
                'name': 'Shiny Colors',
                'd_names': {
                    'ja': 'シャイニーカラーズ',
                },
                'image': 'games/appicons/shanimasu',
                'hashtags': ['シャニマス'],
                'redirect': 'https://www.project-imas.com/wiki/THE_iDOLM@STER:_Shiny_Colors',
            }),
        ]),
    }),
])
