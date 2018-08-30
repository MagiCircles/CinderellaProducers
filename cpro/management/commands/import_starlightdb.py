# -*- coding: utf-8 -*-
from __future__ import division
import json, time, urllib2, requests, datetime
from pprint import pprint
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings as django_settings
from django.core.files.temp import NamedTemporaryFile
from django.core.files.images import ImageFile
from django.core.exceptions import ObjectDoesNotExist
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
    if not url:
        return None
    img_temp = NamedTemporaryFile(delete=True)
    r = requests.get(url)
    # Read the streamed image in sections
    for block in r.iter_content(1024 * 8):
        # If no more file then stop
        if not block:
            break
        # Write image block to temporary file
        img_temp.write(block)
    img_temp.flush()
    return ImageFile(img_temp)

def downloadImage(url, prefix, id, tinypng=False):
    if not url:
        return None
    a = models.uploadItem(prefix)(models.Card.objects.get(id=id), 'lol.png')
    a = a.replace('cpro/static/uploaded/', 'u/')
    return a
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
    1: u'東京',
    2: u'青森',
    3: u'兵庫',
    4: u'大阪',
    5: u'高知',
    6: u'長野',
    7: u'秋田',
    8: u'神奈川',
    9: u'熊本',
    10: u'三重',
    11: u'鳥取',
    12: u'北海道',
    13: u'神戸',
    14: u'新潟',
    15: u'島根',
    16: u'宮崎',
    17: u'富山',
    18: u'千葉',
    19: u'湘南',
    20: u'福井',
    21: u'石川',
    22: u'岩手',
    23: u'岡山',
    24: u'パリ',
    25: u'京都',
    26: u'香港',
    27: u'岐阜',
    28: u'名古屋',
    29: u'奈良',
    30: u'765プロダクション',
    31: u'愛媛',
    32: u'群馬',
    33: u'山形',
    34: u'山梨',
    35: u'滋賀',
    36: u'香川',
    37: u'ウサミン星',
    38: u'佐賀',
    39: u'仙台',
    40: u'静岡',
    41: u'宮城',
    42: u'長崎',
    43: u'福岡',
    44: u'福島',
    45: u'茨城',
    46: u'大分',
    47: u'広島',
    48: u'愛知',
    49: u'ドバイ',
    50: u'海の向こう',
    51: u'和歌山',
    52: u'イギリス',
    53: u'沖縄',
    54: u'埼玉',
    55: u'栃木',
    56: u'山口',
    57: u'鹿児島',
    58: u'リオ・デ・ジャネイロ',
    59: u'サンフランシスコ',
    60: u'ニューヨーク',
    61: u'徳島',
    62: u'グリーンランド',
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
    'all': models.LEADER_SKILL_BRILLIANCE,
    'life': models.LEADER_SKILL_ENERGY,
    'skill_probability': models.LEADER_SKILL_ABILITY,
    '<missing string: 0>': models.LEADER_SKILL_CINDERELLA_CHARM,
    # Note: no way to detect LEADER_SKILL_FORTUNE_PRESENT from LEADER_SKILL_CINDERELLA_CHARM at the moment
}

def getIdolFromJson(owner, chara, update=False):
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
                data['idol'] = getIdolFromJson(owner, card['chara'], update='update' in args)
                data['i_rarity'] = RARITIES[card['rarity']['rarity']]
                data['title'] = card['title']
                if 'images' in args:
                    data['image'] = downloadImage(card['card_image_ref'], 'c', data['id'])
                    data['art'] = downloadImage(card['spread_image_ref'], 'c/art', data['id'])
                    data['transparent'] = downloadImage(card['sprite_image_ref'], 'c/transparent', data['id'])
                    data['icon'] = downloadImage(card['icon_image_ref'], 'c/icon', data['id'])
                    data['puchi'] = downloadImage(card['icon_image_ref'].replace('icon_card', 'puchi'), 'c/puchi', data['id'])
                    if awakened:
                        data['image_awakened'] = downloadImage(awakened['card_image_ref'], 'c/a', data['id'])
                        data['art_awakened'] = downloadImage(awakened['spread_image_ref'], 'c/art/a', data['id'])
                        data['transparent_awakened'] = downloadImage(awakened['sprite_image_ref'], 'c/transparent/a', data['id'])
                        data['icon_awakened'] = downloadImage(awakened['icon_image_ref'], 'c/icon/a', data['id'])
                        data['puchi_awakened'] = downloadImage(awakened['icon_image_ref'].replace('icon_card', 'puchi'), 'c/puchi/a', data['id'])
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
                    data['skill_value2'] = card['skill'][
                        'value_2'
                        if card['skill']['skill_type'] in [
                                'Tricolor Synergy',
                                'All Round',
                                'Focus',
                        ]
                        else 'skill_trigger_value'
                    ]
                    if card['skill']['skill_type'] == 'Focus':
                        data['skill_value2'] = data['skill_value2'] / 100
                    data['skill_value3'] = card['skill']['value_3']
                if 'lead_skill' in card and card['lead_skill']:
                    data['leader_skill_type'] = LEADER_SKILLS[card['lead_skill']['target_param']]

                    if card['lead_skill']['target_param'] == 'life' and (
                            card['lead_skill']['need_cute']
                            or card['lead_skill']['need_cool']
                            or card['lead_skill']['need_passion']
                    ):
                        data['leader_skill_type'] = models.LEADER_SKILL_CHEER

                    if card['lead_skill']['target_param'] == 'all' and (
                            card['lead_skill']['need_cute']
                            or card['lead_skill']['need_cool']
                            or card['lead_skill']['need_passion']
                    ):
                        data['leader_skill_type'] = models.LEADER_SKILL_PRINCESS

                    data['leader_skill_percent'] = card['lead_skill']['up_value']
                    if card['lead_skill']['target_attribute'] == 'all':
                        data['leader_skill_apply'] = models.LEADER_SKILL_APPLIES_TRICOLOR
                        if (not card['lead_skill']['need_cute']
                            and not card['lead_skill']['need_cool']
                            and not card['lead_skill']['need_passion']):
                            data['leader_skill_apply'] = models.LEADER_SKILL_APPLIES_SHINY
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
