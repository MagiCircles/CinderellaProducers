# -*- coding: utf-8 -*-
from __future__ import division
import json, time, urllib2, requests, datetime
from pprint import pprint
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings as django_settings
from django.db.models import Q
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
    print '      Compressing...'
    img_shrunked = NamedTemporaryFile(delete=False)
    shrink_info = shrink_file(
        picture.name,
        api_key=api_key,
        out_filepath=img_shrunked.name
    )
    img_shrunked.flush()
    print '      Done.'
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

def downloadImage(url, prefix, id, tinypng=True):
    if not url:
        return None
    a = models.uploadItem(prefix)(models.Card.objects.get(id=id), 'lol.png')
    a = a.replace('cpro/static/uploaded/', 'u/')
    print '    Downloading', url, '...'
    downloaded = downloadImageFile(url)
    print '    Done.'
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
}

LEADER_SKILLS_BY_NAME = {
    u'シンデレラチャーム': models.LEADER_SKILL_CINDERELLA_CHARM,
    u'フォーチュンプレゼント': models.LEADER_SKILL_FORTUNE_PRESENT,
}

IDOLS_TYPOED_NAMES = {
    u'Oota Yu': u'Ohta Yuu',
    u'Oohara Michiru': u'Ohara Michiru',
    u'Ooishi Izumi': u'Ohishi Izumi',
    u'Ootsuki Yui': u'Ohtsuki Yui',
    u'Eto Misaki': u'Etou Misaki',
    u'Nanba Emi': u'Namba Emi',
    u'Asano Fuuka': u'Asano Fuka',
    u'Cathy Graham': u'Graham Cathy',
}

def getIdolFromJson(owner, chara, update=False, updated_idols=[]):
    name = chara['conventional']
    if name in IDOLS_TYPOED_NAMES:
        name = IDOLS_TYPOED_NAMES[name]
    try:
        idol = models.Idol.objects.get(name=name)
    except ObjectDoesNotExist:
        idol = None
    if idol and not update:
        return idol
    if idol:
        if idol.id in updated_idols:
            return idol
        print 'Updading idol', idol.id, idol, '...'
    else:
        print 'Adding new idol', name, '...'
    data = {
        'owner': owner,
    }
    #data['id'] = chara['chara_id']
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
    updated_idols.append(idol.id)
    print 'Done.'
    return idol

def import_cards(args, cards=[]):
    updated_idols = []

    try:
        owner = models.User.objects.get(username='db0')
    except ObjectDoesNotExist:
        owner = models.User.objects.create(username='db0')
        preferences = UserPreferences.objects.create(user=owner)

    if cards:
        card_ids = [(int(card), int(card) + 1) for card in cards]
    else:
        print 'Downloading list of cards...'
        if 'local' in args:
            f = open('cards.json', 'r')
            result = json.loads(f.read())
        else:
            r = requests.get('https://starlight.kirara.ca/api/v1/list/card_t')
            result = r.json()
        card_ids = [(card['id'], card.get('evolution_id', None)) for card in result['result']]
        print len(card_ids), 'cards have been found (not including awakaning)'
        print 'Done.'
    if 'update' not in args and not cards:
        # Check if already exist
        original_card_ids = card_ids
        exist = [
            (int(id), int(id_awakened))
            for id, id_awakened in
            models.Card.objects.filter(id__in=dict(card_ids).keys()).values_list('id', 'id_awakened')
        ]
        extra_in_db = models.Card.objects.exclude(id__in=dict(card_ids).keys())
        for card in extra_in_db:
            print 'WARNING: This card is in the database but not in the server:', (card.id, card.id_awakened), card
        card_ids = list(set(card_ids) ^ set(exist))
        card_ids = [ids for ids in card_ids if ids in original_card_ids]
        if card_ids:
            print 'Adding', len(card_ids), 'new cards...'
        else:
            print 'No new card available. Use "update" argument to update existing cards.'
    else:
        print 'Adding or updating', len(card_ids), 'cards...'

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
            if not card:
                print 'ERROR: A card has been not found'
                continue
            if card['id'] in card_ids_dict.keys():
                if 'update' in args:
                    print 'Adding or updating card', card['id'], '...'
                else:
                    print 'Adding card', card['id'], '...'
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
                data['idol'] = getIdolFromJson(owner, card['chara'], update='update' in args, updated_idols=updated_idols)
                data['i_rarity'] = RARITIES[card['rarity']['rarity']]
                data['title'] = card['title']
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
                    skill = card['skill']['skill_type']
                    if skill in ['Cute Focus', 'Cool Focus', 'Passion Focus']:
                        skill = 'Cute/Cool/Passion Focus'
                    skill = skill.replace('-', ' ')
                    data['i_skill'] = models.SKILL_REVERSE_DICT[skill]
                    data['skill_name'] = card['skill']['skill_name']
                    data['trigger_value'] = card['skill']['condition']
                    data['trigger_chance_min'] = card['skill']['proc_chance'][0] / 100
                    data['trigger_chance_max'] = card['skill']['proc_chance'][1] / 100
                    data['skill_duration_min'] = card['skill']['effect_length'][0] / 100
                    data['skill_duration_max'] = card['skill']['effect_length'][1] / 100
                    data['skill_value'] = card['skill']['value'] - 100 if data['i_skill'] != models.SKILL_HEALER else card['skill']['value']
                    data['skill_value2'] = card['skill'][
                        'value_2'
                        if skill in [
                                'Tricolor Synergy',
                                'All Round',
                                'Cute/Cool/Passion Focus',
                                'Focus',
                        ]
                        else 'skill_trigger_value'
                    ]
                    if skill in [
                            'Tricolor Synergy',
                            'Cute/Cool/Passion Focus',
                            'Focus',
                    ]:
                        data['skill_value2'] = data['skill_value2'] - 100
                    data['skill_value3'] = card['skill']['value_3']
                if 'lead_skill' in card and card['lead_skill']:
                    if card['lead_skill']['name'] in LEADER_SKILLS_BY_NAME:
                        data['leader_skill_type'] = LEADER_SKILLS_BY_NAME[card['lead_skill']['name']]
                    else:
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
                    if (card['lead_skill']['target_attribute'] == 'all'
                        and data['leader_skill_type'] not in models.LEADER_SKILLS_WITHOUT_PREFIX):
                        data['leader_skill_apply'] = models.LEADER_SKILL_APPLIES_TRICOLOR
                        if (not card['lead_skill']['need_cute']
                            and not card['lead_skill']['need_cool']
                            and not card['lead_skill']['need_passion']):
                            data['leader_skill_apply'] = models.LEADER_SKILL_APPLIES_SHINY
                    else:
                        data['leader_skill_apply'] = models.LEADER_SKILL_APPLIES_TYPE
                new_card, created = models.Card.objects.update_or_create(id=card['id'], defaults=data)
                print '  -> Card', 'added' if created else 'updated', new_card.id, new_card
                if 'images' in args:
                    print '  Adding images to card...'
                    if not new_card.image or 'update' in args:
                        new_card.image = downloadImage(card['card_image_ref'], 'c', new_card.id)
                    if not new_card.art or 'update' in args:
                        new_card.art = downloadImage(card['spread_image_ref'], 'c/art', new_card.id)
                    if not new_card.transparent or 'update' in args:
                        new_card.transparent = downloadImage(card['sprite_image_ref'], 'c/transparent', new_card.id)
                    if not new_card.icon or 'update' in args:
                        new_card.icon = downloadImage(card['icon_image_ref'], 'c/icon', new_card.id)
                    if not new_card.puchi or 'update' in args:
                        new_card.puchi = downloadImage(card['icon_image_ref'].replace('icon_card', 'puchi'), 'c/puchi', new_card.id)
                    if awakened:
                        if not new_card.image_awakened or 'update' in args:
                            new_card.image_awakened = downloadImage(awakened['card_image_ref'], 'c/a', new_card.id)
                        if not new_card.art_awakened or 'update' in args:
                            new_card.art_awakened = downloadImage(awakened['spread_image_ref'], 'c/art/a', new_card.id)
                        if not new_card.transparent_awakened or 'update' in args:
                            new_card.transparent_awakened = downloadImage(awakened['sprite_image_ref'], 'c/transparent/a', new_card.id)
                        if not new_card.icon_awakened or 'update' in args:
                            new_card.icon_awakened = downloadImage(awakened['icon_image_ref'], 'c/icon/a', new_card.id)
                        if not new_card.puchi_awakened or 'update' in args:
                            new_card.puchi_awakened = downloadImage(awakened['icon_image_ref'].replace('icon_card', 'puchi'), 'c/puchi/a', new_card.id)
                    print '  Done.'
                    print '  Uploading downloaded images and saving card...'
                    new_card.save()
                    print '  Done.'
        card_ids = card_ids[10:]
        i += 1
    print 'Done.'

def import_starlightdb(args, cards=[]):

    if 'skip_cards' not in args:
        import_cards(args, cards)

    if 'skip_idol_images' not in args:
        print 'Saving idols images...'
        i = 0
        e = 0
        for idol in models.Idol.objects.all():
            try:
                if not idol.image or 'update' in args:
                    idol.image = unicode(models.Card.objects.filter(idol=idol, puchi__isnull=False).exclude(puchi='').order_by('id')[0].puchi)
                    idol.save()
                    print 'Idol image has been updated for', idol.id, idol
                    i += 1
            except IndexError:
                print 'WARNING: Idol', idol.id, idol, 'does not have any card that has a puchi image, so no image has been saved.'
                e += 1
        print i, 'idols images updated and', e, 'errors'
        print 'Done.'

    if 'skip_translations' not in args:
        print 'Getting strings that need to be translated...'
        translated_fields = ['title', 'skill_name']
        q = Q()
        for field in translated_fields:
            q |= (Q(**{ u'{}__isnull'.format(field): False }) & ~Q(**{ field: '' })
                  & (Q(**{ u'translated_{}__isnull'.format(field): True })
                     | Q(**{ u'translated_{}'.format(field): '' })))
        cards_need_translations = models.Card.objects.filter(q)
        print '  ', cards_need_translations.count(), 'cards are missing the translation of their title or skill name or both.'
        translations = {}# term: {} for term in translated_terms }
        # { 'hello world': { 'title': [card1, card2, ...], 'skill': [card6, ...] }, ... }
        for card in cards_need_translations:
            for field in translated_fields:
                string = getattr(card, field)
                if string and not getattr(card, u'translated_{}'.format(field)):
                    if string not in translations:
                        translations[string] = { field: [] for field in translated_fields }
                    translations[string][field].append(card)
        print '  Total fields that need translations: ', len(translations)
        print 'Done.'
        print 'Downloading translations...'
        r = requests.post('https://starlight.kirara.ca/api/v1/read_tl', data=json.dumps(translations.keys()))
        result = r.json()
        for string, fields in translations.items():
            if string not in result:
                total_affected = reduce(lambda a, b: a + b, [len(c) for c in fields.values()])
                print '  WARNING: No translation found for "', string, '" (', total_affected, 'cards fields affected)'
                continue
            for field, cards in fields.items():
                for card in cards:
                    print '  Card', card.id, card, field, string, '->', result[string]
                    setattr(card, 'translated_{}'.format(field), result[string])
                    card.save()
        print 'Done.'

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        cards = []
        for arg in args:
            if arg.isdigit():
                cards.append(arg)
            else:
                break
        import_starlightdb(args, cards=cards)
