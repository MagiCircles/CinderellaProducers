# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _, string_concat

############################################################
# User

DONATORS_STATUS_CHOICES = (
    ('THANKS', 'Thanks'),
    ('SUPPORTER', _('Skilled Producer')),
    ('LOVER', _('Expert Producer')),
    ('AMBASSADOR', _('Veteran Producer')),
    ('PRODUCER', _('Ultimate Producer')),
    ('DEVOTEE', _('Idol Master')),
)
DONATORS_STATUS_DICT = dict(DONATORS_STATUS_CHOICES)

############################################################
# Idol

TYPE_CUTE = 0
TYPE_COOL = 1
TYPE_PASSION = 2

TYPES = [
    (TYPE_CUTE, _('Cute'), 'Cute', '#FF0173'),
    (TYPE_COOL, _('Cool'), 'Cool', '#0E75FF'),
    (TYPE_PASSION, _('Passion'), 'Passion', '#FFAA00'),
]
TYPE_CHOICES = [(a, b) for (a, b, c, d) in TYPES]
TYPE_DICT = dict(TYPE_CHOICES)

ENGLISH_TYPE_DICT = {
    TYPE_CUTE: 'Cute',
    TYPE_COOL: 'Cool',
    TYPE_PASSION: 'Passion',
}

STAT_VOCAL = 0
STAT_DANCE = 1
STAT_VISUAL = 2

STAT_CHOICES = [
    (STAT_VOCAL, _('Vocal')),
    (STAT_DANCE, _('Dance')),
    (STAT_VISUAL, _('Visual')),
]
STAT_DICT = dict(STAT_CHOICES)

BLOOD_TYPES = [ 'O', 'A', 'B', 'AB' ]
BLOOD_TYPE_CHOICES = list(enumerate(BLOOD_TYPES))
BLOOD_TYPE_DICT = dict(BLOOD_TYPE_CHOICES)
BLOOD_TYPE_REVERSE_DICT = { value: key for (key, value) in BLOOD_TYPE_CHOICES }

WRITING_HANDS = [ _('Right'), _('Left'), _('Both') ]
UNTRANSLATED_WRITING_HANDS = [ 'Right', 'Left', 'Both' ]
WRITING_HAND_CHOICES = list(enumerate(WRITING_HANDS))
WRITING_HANDS_DICT = dict(WRITING_HAND_CHOICES)
WRITING_HANDS_REVERSE_DICT = { value: key for (key, value) in list(enumerate(UNTRANSLATED_WRITING_HANDS)) }

UNTRANSLATED_ASTROLOGICAL_SIGNS = [
    'Leo',
    'Aries',
    'Libra',
    'Virgo',
    'Scorpio',
    'Capricorn',
    'Pisces',
    'Gemini',
    'Cancer',
    'Sagittarius',
    'Aquarius',
    'Taurus',
]
UNTRANSLATED_ASTROLOGICAL_SIGN_CHOICES = list(enumerate(UNTRANSLATED_ASTROLOGICAL_SIGNS))
UNTRANSLATED_ASTROLOGICAL_SIGN_DICT = dict(UNTRANSLATED_ASTROLOGICAL_SIGN_CHOICES)
ASTROLOGICAL_SIGN_REVERSE_DICT = { value: key for (key, value) in list(enumerate(UNTRANSLATED_ASTROLOGICAL_SIGNS)) }
ASTROLOGICAL_SIGNS = [
    _('Leo'),
    _('Aries'),
    _('Libra'),
    _('Virgo'),
    _('Scorpio'),
    _('Capricorn'),
    _('Pisces'),
    _('Gemini'),
    _('Cancer'),
    _('Sagittarius'),
    _('Aquarius'),
    _('Taurus'),
]
ASTROLOGICAL_SIGN_CHOICES = list(enumerate(ASTROLOGICAL_SIGNS))
ASTROLOGICAL_SIGN_DICT = dict(ASTROLOGICAL_SIGN_CHOICES)

############################################################
# Event

EVENT_KINDS = [
    _('Token'),
    _('Medley'),
    _('Coop'),
    _('Caravan'),
    _('LIVE Parade'),
]
EVENT_KIND_CHOICES = list(enumerate(EVENT_KINDS))
EVENT_KIND_DICT = dict(EVENT_KIND_CHOICES)

############################################################
# Card

RARITY_N = 0
RARITY_R = 1
RARITY_SR = 2
RARITY_SSR = 3

RARITY_CHOICES = [
    (RARITY_N, _('Normal')),
    (RARITY_R, _('Rare')),
    (RARITY_SR, _('Super Rare')),
    (RARITY_SSR, _('Super Super Rare')),
]
RARITY_DICT = dict(RARITY_CHOICES)

RARITY_SHORT_DICT = {
    RARITY_N: 'N',
    RARITY_R: 'R',
    RARITY_SR: 'SR',
    RARITY_SSR: 'SSR',
}

MAX_LEVELS = {
    RARITY_N: (20, 30),
    RARITY_R: (40, 50),
    RARITY_SR: (60, 70),
    RARITY_SSR: (80, 90),
}

MAX_SKILL_LEVEL = 10

SKILL_LESSER_PERFECT_LOCK = 0
SKILL_GREATER_PERFECT_LOCK = 1
SKILL_EXTREME_PERFECT_LOCK = 2
SKILL_COMBO_LOCK = 3
SKILL_HEALER = 4
SKILL_LIFE_GUARD = 5
SKILL_COMBO_BONUS = 6
SKILL_PERFECT_SCORE_BONUS = 7
SKILL_OVERLOAD = 8
SKILL_SCORE_BOOST = 9
SKILL_ALL_ROUND = 10
SKILL_CONCENTRATION = 11
SKILL_SKILL_BOOST = 12
SKILL_FOCUS = 13

SKILL_CHOICES = [
    (SKILL_LESSER_PERFECT_LOCK, _('Lesser Perfect Lock')),
    (SKILL_GREATER_PERFECT_LOCK, _('Greater Perfect Lock')),
    (SKILL_EXTREME_PERFECT_LOCK, _('Extreme Perfect Lock')),
    (SKILL_COMBO_LOCK, _('Combo Lock')),
    (SKILL_HEALER, _('Healer')),
    (SKILL_LIFE_GUARD, _('Life Lock')),
    (SKILL_COMBO_BONUS, _('Combo Bonus')),
    (SKILL_PERFECT_SCORE_BONUS, _('Perfect Score Bonus')),
    (SKILL_OVERLOAD, _('Overload')),
    (SKILL_SCORE_BOOST, _('Score Boost')),
    (SKILL_ALL_ROUND, _('All Round')),
    (SKILL_CONCENTRATION, _('Concentration')),
    (SKILL_SKILL_BOOST, _('Skill Boost')),
    (SKILL_FOCUS, _('Cute/Cool/Passion Focus')),
]
SKILL_DICT = dict(SKILL_CHOICES)
UNTRANSLATED_SKILL_CHOICES = [
    (SKILL_LESSER_PERFECT_LOCK, 'Lesser Perfect Lock'),
    (SKILL_GREATER_PERFECT_LOCK, 'Greater Perfect Lock'),
    (SKILL_EXTREME_PERFECT_LOCK, 'Extreme Perfect Lock'),
    (SKILL_COMBO_LOCK, 'Combo Guard'),
    (SKILL_HEALER, 'Healer'),
    (SKILL_LIFE_GUARD, 'Life Guard'),
    (SKILL_COMBO_BONUS, 'Combo Bonus'),
    (SKILL_PERFECT_SCORE_BONUS, 'Perfect Score Bonus'),
    (SKILL_OVERLOAD, 'Overload'),
    (SKILL_SCORE_BOOST, 'Score Bonus'),
    (SKILL_ALL_ROUND, 'All Round'),
    (SKILL_CONCENTRATION, 'Concentration'),
    (SKILL_SKILL_BOOST, 'Skill Boost'),
    (SKILL_FOCUS, 'Cute/Cool/Passion Focus'),
]
SKILL_REVERSE_DICT = { value: key for (key, value) in UNTRANSLATED_SKILL_CHOICES }

SKILL_SENTENCES = {
    SKILL_LESSER_PERFECT_LOCK: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance of turning all Great notes into Perfect notes in the next {skill_duration} seconds.'),
    SKILL_GREATER_PERFECT_LOCK: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance of turning all Nice and Great notes into Perfect notes in the next {skill_duration} seconds.'),
    SKILL_EXTREME_PERFECT_LOCK: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance of turning all Bad, Nice and Great notes into Perfect notes in the next {skill_duration} seconds.'),
    SKILL_COMBO_LOCK: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance that Nice notes will not break the combo in the next {skill_duration} seconds.'),
    SKILL_HEALER: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance that Perfect notes will restore {skill_value} life in the next {skill_duration} seconds.'),
    SKILL_LIFE_GUARD: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance that you will not lose health in the next {skill_duration} seconds.'),
    SKILL_COMBO_BONUS: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance that you will gain an extra {skill_value}% combo bonus in the next {skill_duration} seconds.'),
    SKILL_PERFECT_SCORE_BONUS: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance that Perfect notes will receive a {skill_value}% score bonus in the next {skill_duration} seconds.'),
    SKILL_OVERLOAD: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance that Perfect notes will receive a {skill_value}% bonus and Nice and Bad notes will not break your combo in the next {skill_duration} seconds, at the cost of {skill_value2} life.'),
    SKILL_SCORE_BOOST: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance that Great and Perfect notes will receive a {skill_value}% score bonus in the next {skill_duration} seconds.'),
    SKILL_ALL_ROUND: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance that you will gain an extra {skill_value}% combo bonus and Perfect notes will restore {skill_value2} life in the next {skill_duration} seconds.'),
    SKILL_CONCENTRATION: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance that Perfect notes will receive a {skill_value}% score bonus but the timing window for Perfect notes is reduced in the next {skill_duration} seconds.'),
    SKILL_SKILL_BOOST: _('For every {trigger_value} seconds, there is a {trigger_chance}% change that currently active skills will be boosted for {skill_duration} seconds'),
    SKILL_FOCUS: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance that Perfect notes will receive a {skill_value}% score bonus, and you will gain an extra {skill_value2}% combo bonus, but only if you have {type} idols in your team'),
}

JAPANESE_SKILL_SENTENCES = {
    SKILL_LESSER_PERFECT_LOCK: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、GREATをPERFECTにする',
    SKILL_GREATER_PERFECT_LOCK: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、GREAT/NICEをPERFECTにする',
    SKILL_EXTREME_PERFECT_LOCK: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、GREAT/NICE/BADをPERFECTにする',
    SKILL_COMBO_LOCK: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、NICEでもCOMBOが継続する',
    SKILL_HEALER: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、PERFECTでライフ{skill_value}回復',
    SKILL_LIFE_GUARD: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、ライフが減少しなくなる',
    SKILL_COMBO_BONUS: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、COMBOボーナス{skill_value}%アップ',
    SKILL_PERFECT_SCORE_BONUS: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、PERFECTのスコア{skill_value}%アップ',
    SKILL_OVERLOAD: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、中確率でライフを{skill_value2}消費し、間PERFECTのスコア{skill_value}%アップ、NICE/BADでもCOMBO継続',
    SKILL_SCORE_BOOST: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、PERFECT/GREATのスコア{skill_value}%アップ',
    SKILL_ALL_ROUND: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、COMBOボーナス{skill_value}%アップ、PERFECTでライフ{skill_value2}回復',
    SKILL_CONCENTRATION: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、高確率でわずかな間、PERFECTのスコア{skill_value}%アップ、PERFECT判定される時間が短くなる',
    SKILL_SKILL_BOOST: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌{trigger_value}秒毎、高確率でしばらくの間、他アイドルの特技効果を大アップ',
    SKILL_FOCUS: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌(キュート/クール/パッション)アイドルのみ編成時、{trigger_value}秒毎、高確率でしばらくの間、PERFECTのスコア{skill_value}%アップ、COMBOボーナス{skill_value2}%アップ',
}

LEADER_SKILL_SENTENCE = _('Raises {leader_skill_type} of all {idol_type} idols by {leader_skill_percent}%.')
JAPANESE_LEADER_SKILL_SENTENCE = u'{idol_type}の{leader_skill_type}{leader_skill_percent}％アップ'

LEADER_SKILL_ALL = 101
LEADER_SKILL_LIFE = 102
LEADER_SKILL_SKILL = 103

LEADER_SKILL_CHOICES = STAT_CHOICES + [
    (LEADER_SKILL_ALL, _('All')),
    (LEADER_SKILL_LIFE, _('Life')),
    (LEADER_SKILL_SKILL, _('Skill')),
]
LEADER_SKILL_DICT = dict(LEADER_SKILL_CHOICES)

JAPANESE_LEADER_SKILL_STAT_IN_SENTENCE = {
    STAT_VOCAL: u'ボーカルアピール値',
    STAT_VISUAL: u'ビジュアルアピール値',
    STAT_DANCE: u'ダンスアピール値',
    LEADER_SKILL_LIFE: u'ライフ',
    LEADER_SKILL_SKILL: u'特技発動確率',
    LEADER_SKILL_ALL: u'全アピール値',
}

TRANSLATED_LEADER_SKILL_STAT_IN_SENTENCE = {
    STAT_VOCAL: _('Vocal'),
    STAT_VISUAL: _('Visual'),
    STAT_DANCE: _('Dance'),
    LEADER_SKILL_LIFE: _('Life'),
    LEADER_SKILL_SKILL: _('Skill'),
    LEADER_SKILL_ALL: string_concat(_('Vocal'), '/', _('Visual'), '/', _('Dance')),
}

JAPANESE_LEADER_SKILL_STAT = {
    STAT_VOCAL: u'ボイス',
    STAT_VISUAL: u'メイク',
    STAT_DANCE: u'ステップ',
    LEADER_SKILL_LIFE: u'エナジー',
    LEADER_SKILL_SKILL: u'アビリティ',
    LEADER_SKILL_ALL: u'ブリリアンス',
}

TRANSLATED_LEADER_SKILL_STAT = {
    STAT_VOCAL: _('Voice'),
    STAT_VISUAL: _('Make-Up'),
    STAT_DANCE: _('Step'),
    LEADER_SKILL_LIFE: _('Energy'),
    LEADER_SKILL_SKILL: _('Ability'),
    LEADER_SKILL_ALL: _('Brilliance'),
}

JAPANESE_TYPES = {
    TYPE_CUTE: u'キュート',
    TYPE_COOL: u'クール',
    TYPE_PASSION: u'パッション',
}

JAPANESE_LEADER_SKILL_RARITY_ALL = {
    RARITY_SR: u'シャイニー',
    RARITY_SSR: u'トリコロール・',
}

TRANSLATED_LEADER_SKILL_RARITY_ALL = {
    RARITY_SR: _('Shiny'),
    RARITY_SSR: _('Tricolor'),
}

JAPANESE_LEADER_SKILL_RARITY_ALL_IN_SENTENCE = {
    RARITY_SR: u'全員',
    RARITY_SSR: u'3タイプ全てのアイドル編成時、全員',
}

TRANSLATED_LEADER_SKILL_RARITY_ALL_IN_SENTENCE = {
    RARITY_SR: _('Shiny'),
    RARITY_SSR: _('Tricolor'),
}

############################################################
# Account

PLAY_WITH = (
    (_('Thumbs'), 'thumbs'),
    (_('All fingers'), 'fingers'),
    (_('Index fingers'), 'index'),
    (_('One hand'), 'fingers'),
    (_('Other'), 'sausage'),
)
PLAY_WITH_CHOICES = [ (index, localized) for (index, (localized, _)) in enumerate(PLAY_WITH) ]
PLAY_WITH_DICT = dict(PLAY_WITH_CHOICES)
PLAY_WITH_ICONS = dict([ (index, icon) for (index, (_, icon)) in enumerate(PLAY_WITH) ])

OS = [ 'iOs', 'Android' ]
OS_CHOICES = list(enumerate(OS))
OS_DICT = dict(OS_CHOICES)

PRODUCER_RANK = [
    'E', 'D', 'C', 'B', 'A', 'S', 'SS'
]
PRODUCER_RANK_CHOICES = list(enumerate(PRODUCER_RANK))
PRODUCER_RANK_DICT = dict(PRODUCER_RANK_CHOICES)
