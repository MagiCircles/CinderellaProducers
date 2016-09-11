# -*- coding: utf-8 -*-
import json, time, urllib2, requests, datetime
from pprint import pprint
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings as django_settings
from django.core.files.temp import NamedTemporaryFile
from django.core.files.images import ImageFile
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from tinypng import shrink_file
from web.models import UserPreferences
from cpro import models

def shrunkImage(picture, filename):
    api_key = django_settings.TINYPNG_API_KEY
    if not api_key or not filename.endswith('.png'):
        return picture
    img_shrunked = NamedTemporaryFile(delete=False)
    shrink_info = shrink_file(
        picture.name,
        api_key=api_key,
        out_filepath=img_shrunked.name
    )
    img_shrunked.flush()
    return ImageFile(img_shrunked)

def downloadImageFile(url):
    img_temp = NamedTemporaryFile(delete=True)
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36' })
    img_temp.write(urllib2.urlopen(req).read())
    img_temp.flush()
    return ImageFile(img_temp)

def downloadImage(url, tinypng=False):
    downloaded = downloadImageFile(url)
    if tinypng:
        return shrunkImage(downloaded, url)
    return downloaded

TYPE_STRINGS = {
    'cute': models.TYPE_CUTE,
    'cool': models.TYPE_COOL,
    'passion': models.TYPE_PASSION,
}

BLOOD_TYPES = {
    2001: 'A',
    2002: 'B',
    2003: 'AB',
    2004: 'O',
}

WRITING_HANDS = {
    3001: 'Right',
    3002: 'Left',
    3003: 'Both',
}

ASTROLOGICAL_SIGNS = {
    1001: 'Taurus',
    1002: 'Aries',
    1003: 'Libra',
    1004: 'Aquarius',
    1005: 'Pisces',
    1006: 'Virgo',
    1007: 'Capricorn',
    1008: 'Gemini',
    1009: 'Scorpio',
    1010: 'Sagittarius',
    1011: 'Leo',
    1012: 'Cancer',
    1013: 'Virgo',
    1014: 'Cancer',
}

HOMETOWNS = {
    1: _(u'東京'),
    2: _(u'青森'),
    3: _(u'兵庫'),
    4: _(u'大阪'),
    5: _(u'高知'),
    6: _(u'長野'),
    7: _(u'秋田'),
    8: _(u'神奈川'),
    9: _(u'熊本'),
    10: _(u'三重'),
    11: _(u'鳥取'),
    12: _(u'北海道'),
    13: _(u'神戸'),
    14: _(u'新潟'),
    15: _(u'島根'),
    16: _(u'宮崎'),
    17: _(u'富山'),
    18: _(u'千葉'),
    19: _(u'湘南'),
    20: _(u'福井'),
    21: _(u'石川'),
    22: _(u'岩手'),
    23: _(u'岡山'),
    24: _(u'パリ'),
    25: _(u'京都'),
    26: _(u'香港'),
    27: _(u'岐阜'),
    28: _(u'名古屋'),
    29: _(u'奈良'),
    30: _(u'765プロダクション'),
    31: _(u'愛媛'),
    32: _(u'群馬'),
    33: _(u'山形'),
    34: _(u'山梨'),
    35: _(u'滋賀'),
    36: _(u'香川'),
    37: _(u'ウサミン星'),
    38: _(u'佐賀'),
    39: _(u'仙台'),
    40: _(u'静岡'),
    41: _(u'宮城'),
    42: _(u'長崎'),
    43: _(u'福岡'),
    44: _(u'福島'),
    45: _(u'茨城'),
    46: _(u'大分'),
    47: _(u'広島'),
    48: _(u'愛知'),
    49: _(u'ドバイ'),
    50: _(u'海の向こう'),
    51: _(u'和歌山'),
    52: _(u'イギリス'),
    53: _(u'沖縄'),
    54: _(u'埼玉'),
    55: _(u'栃木'),
    56: _(u'山口'),
    57: _(u'鹿児島'),
    58: _(u'リオ・デ・ジャネイロ'),
    59: _(u'サンフランシスコ'),
    60: _(u'ニューヨーク'),
    61: _(u'徳島'),
    62: _(u'グリーンランド'),
}

RARITIES = {
    1: models.RARITY_N,
    2: models.RARITY_N,
    3: models.RARITY_R,
    4: models.RARITY_R,
    5: models.RARITY_SR,
    6: models.RARITY_SR,
    7: models.RARITY_SSR,
    8: models.RARITY_SSR,
}

LEADER_SKILLS = {
    'vocal': models.STAT_VOCAL,
    'visual': models.STAT_VISUAL,
    'dance': models.STAT_DANCE,
    'all': models.LEADER_SKILL_ALL,
    'life': models.LEADER_SKILL_LIFE,
    'skill_probability': models.LEADER_SKILL_SKILL,
}

def getIdolFromJson(owner, chara, update=False, image=True):
    name = chara['conventional']
    try:
        idol = models.Idol.objects.get(name=name)
    except ObjectDoesNotExist:
        idol = None
    if idol and not update:
        return idol
    data = {
        'owner': owner,
    }
    data['id'] = chara['chara_id']
    data['japanese_name'] = chara['name']
    data['i_type'] = TYPE_STRINGS[chara['type']] if chara['type'] in TYPE_STRINGS else None
    if chara['age'] < 200:
        data['age'] = chara['age']
    data['birthday'] = datetime.date(2015, chara['birth_month'], chara['birth_day'])
    data['height'] = chara['height']
    if chara['weight'] < 200:
        data['weight'] = chara['weight']
    data['i_blood_type'] = models.BLOOD_TYPE_REVERSE_DICT[BLOOD_TYPES[chara['blood_type']]]
    data['i_writing_hand'] = models.WRITING_HANDS_REVERSE_DICT[WRITING_HANDS[chara['hand']]]
    data['bust'] = chara['body_size_1']
    data['waist'] = chara['body_size_2']
    data['hips'] = chara['body_size_3']
    data['i_astrological_sign'] = models.ASTROLOGICAL_SIGN_REVERSE_DICT[ASTROLOGICAL_SIGNS[chara['constellation']]]
    data['hometown'] = HOMETOWNS[chara['home_town']]
    data['CV'] = chara['voice'] if chara['voice'] else None
    #if image:
    #    data['image'] = downloadImage(chara['icon_image_ref'])
    idol, created = models.Idol.objects.update_or_create(name=name, defaults=data)
    return idol

def import_starlightdb(args):

    if 'local' in args:
        f = open('cards.json', 'r')
        result = json.loads(f.read())
    else:
        r = requests.get('https://starlight.kirara.ca/api/v1/list/card_t')
        result = r.json()
    try:
        owner = models.User.objects.get(username='db0')
    except ObjectDoesNotExist:
        owner = models.User.objects.create(username='db0')
        preferences = UserPreferences.objects.create(user=owner)
    card_ids = [(card['id'], card.get('evolution_id', None)) for card in result['result']]
    card_ids_dict = dict(card_ids)
    i = 1
    while card_ids:
        url = u'https://starlight.kirara.ca/api/v1/card_t/' + u','.join([u','.join([unicode(id) for id in ids]) for ids in card_ids[:10]])
        if 'local' in args:
            try:
                f = open('cardsPage{}.json'.format(i))
                result = json.loads(f.read())
            except IOError:
                print url
                print 'cardsPage{}.json not found in local files'.format(i)
                card_ids = card_ids[10:]
                i += 1
                continue
        else:
            r = requests.get(url)
            result = r.json()
        for card in result['result']:
            print card['id']
            if card['id'] in card_ids_dict.keys():
                data = {
                    'owner': owner,
                }
                data['id'] = card['id']
                data['id_awakened'] = card_ids_dict[data['id']]
                try:
                    awakened = (c for c in result['result'] if c['id'] == data['id_awakened']).next()
                except StopIteration:
                    awakened = None
                    print ' WARNING: Awakened not found'
                data['idol'] = getIdolFromJson(owner, card['chara'], update='update' in args, image='images' in args)
                data['i_rarity'] = RARITIES[card['rarity']['rarity']]
                data['title'] = card['title']
                if 'images' in args:
                    data['image'] = downloadImage(card['card_image_ref'])
                    data['art'] = downloadImage(card['spread_image_ref'])
                    data['transparent'] = downloadImage(card['sprite_image_ref'])
                    data['icon'] = downloadImage(card['icon_image_ref'])
                    data['puchi'] = downloadImage(card['icon_image_ref'].replace('icon_card', 'puchi'))
                    if awakened:
                        data['image_awakened'] = downloadImage(awakened['card_image_ref'])
                        data['art_awakened'] = downloadImage(awakened['spread_image_ref'])
                        data['transparent_awakened'] = downloadImage(awakened['sprite_image_ref'])
                        data['icon_awakened'] = downloadImage(awakened['icon_image_ref'])
                        data['puchi_awakened'] = downloadImage(awakened['icon_image_ref'].replace('icon_card', 'puchi'))
                data['hp_min'] = card['hp_min']
                data['hp_max'] = card['hp_max']
                data['vocal_min'] = card['vocal_min']
                data['vocal_max'] = card['vocal_max']
                data['dance_min'] = card['dance_min']
                data['dance_max'] = card['dance_max']
                data['visual_min'] = card['visual_min']
                data['visual_max'] = card['visual_max']
                if awakened:
                    data['hp_awakened_min'] = awakened['hp_min']
                    data['hp_awakened_max'] = awakened['hp_max']
                    data['vocal_awakened_min'] =  awakened['vocal_min']
                    data['vocal_awakened_max'] = awakened['vocal_max']
                    data['dance_awakened_min'] =  awakened['dance_min']
                    data['dance_awakened_max'] = awakened['dance_max']
                    data['visual_awakened_min'] =  awakened['visual_min']
                    data['visual_awakened_max'] = awakened['visual_max']
                if 'skill' in card and card['skill']:
                    data['i_skill'] = models.SKILL_REVERSE_DICT[card['skill']['skill_type']]
                    data['skill_name'] = card['skill']['skill_name']
                    data['trigger_value'] = card['skill']['condition']
                    data['trigger_chance_min'] = card['skill']['proc_chance'][0] / 100
                    data['trigger_chance_max'] = card['skill']['proc_chance'][1] / 100
                    data['skill_duration_min'] = card['skill']['effect_length'][0] / 100
                    data['skill_duration_max'] = card['skill']['effect_length'][1] / 100
                    data['skill_value'] = card['skill']['value'] - 100 if data['i_skill'] != models.SKILL_HEALER else card['skill']['value']
                    data['skill_value2'] = card['skill']['skill_trigger_value']
                if 'lead_skill' in card and card['lead_skill']:
                    data['leader_skill_type'] = LEADER_SKILLS[card['lead_skill']['target_param']]
                    data['leader_skill_percent'] = card['lead_skill']['up_value']
                    if card['lead_skill']['target_attribute'] == 'all':
                        data['leader_skill_all'] = True
                card, created = models.Card.objects.update_or_create(id=card['id'], defaults=data)
        card_ids = card_ids[10:]
        i += 1
    print 'Save idols images'
    for idol in models.Idol.objects.all():
        idol.image = unicode(models.Card.objects.filter(idol=idol).order_by('id')[0].puchi)
        idol.save()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        import_starlightdb(args)
