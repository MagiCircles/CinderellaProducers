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

JAPANESE_TYPES = {
    TYPE_CUTE: u'キュート',
    TYPE_COOL: u'クール',
    TYPE_PASSION: u'パッション',
}

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

# SKILL

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
SKILL_ENCORE = 14
SKILL_SPARKLE = 15
SKILL_TRICOLOR_SYNERGY = 16

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
    (SKILL_ENCORE, _('Encore')),
    (SKILL_SPARKLE, _('Sparkle')),
    (SKILL_TRICOLOR_SYNERGY, _('Tricolor Synergy')),
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
    (SKILL_ENCORE, 'Encore'),
    (SKILL_SPARKLE, 'Sparkle'),
    (SKILL_TRICOLOR_SYNERGY, 'Tricolor Synergy'),
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
    SKILL_FOCUS: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance that Perfect notes will receive a {skill_value}% score bonus, and you will gain an extra {skill_value2}% combo bonus, but only if you have only {type} idols in your team for {skill_duration} seconds'),
    SKILL_ENCORE: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance to activate the previous skill again for {skill_duration} seconds.'),
    SKILL_SPARKLE: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance that you will gain an extra combo bonus based on your current health for {skill_duration} seconds.'),
    SKILL_TRICOLOR_SYNERGY: _('For every {trigger_value} seconds, there is a {trigger_chance}% chance that with all three types of idols on the team, you will gain an extra {skill_value}% combo bonus, and Perfect notes will receive a {skill_value2}% score bonus plus restore {skill_value3} life, for {skill_duration} seconds.'),
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
    SKILL_FOCUS: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌{type}アイドルのみ編成時、{trigger_value}秒毎、高確率でしばらくの間、PERFECTのスコア{skill_value}%アップ、COMBOボーナス{skill_value2}%アップ',
    SKILL_ENCORE: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌{trigger_value}秒毎、直前に発動した他アイドルの特技効果を繰り返す',
    SKILL_SPARKLE: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌{trigger_value}秒毎、ライフ値が多いほどCOMBOボーナスアップ',
    SKILL_TRICOLOR_SYNERGY: u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌3タイプ全てのアイドル編成時、{trigger_value}秒毎、PERFECTのスコア{skill_value}%アップ/ライフ{skill_value3}回復、COMBOボーナス{skill_value2}%アップ',
}

# LEADER SKILL

# Type of skill

LEADER_SKILL_BRILLIANCE = 101
LEADER_SKILL_ENERGY = 102
LEADER_SKILL_ABILITY = 103
LEADER_SKILL_CHEER = 104
LEADER_SKILL_PRINCESS = 105
LEADER_SKILL_CINDERELLA_CHARM = 106
LEADER_SKILL_FORTUNE_PRESENT = 107

LEADER_SKILL_CHOICES = [
    (STAT_VOCAL, 'Vocal appeal [Voice]'),
    (STAT_VISUAL, 'Visual appeal [Make-up]'),
    (STAT_DANCE, 'Dance appeal [Step]'),
    (LEADER_SKILL_BRILLIANCE, 'Vocal/Visual/Dance appeals [Brilliance]'),
    (LEADER_SKILL_PRINCESS, 'Vocal/Visual/Dance appeals, when only same type in the team [Princess]'),
    (LEADER_SKILL_ABILITY, 'Skill probability [Ability]'),
    (LEADER_SKILL_ENERGY, 'Life [Energy]'),
    (LEADER_SKILL_CHEER, 'Life, when only same type in the team [Cheer]'),
    (LEADER_SKILL_CINDERELLA_CHARM, 'Fan gain, end of live [Cinderella Charm]'),
    (LEADER_SKILL_FORTUNE_PRESENT, 'Rewards, end of live [Fortune Present]'),
]
LEADER_SKILL_DICT = dict(LEADER_SKILL_CHOICES)

# Applies to

LEADER_SKILL_APPLIES_TYPE = None
LEADER_SKILL_APPLIES_TRICOLOR = 1
LEADER_SKILL_APPLIES_SHINY = 2

LEADER_SKILL_APPLIES_CHOICES = [
    (LEADER_SKILL_APPLIES_TYPE, 'Idols of the same type [Cute/Cool/Passion]'),
    (LEADER_SKILL_APPLIES_TRICOLOR, 'Idols of all 3 types, when all types are in the team [Tricolor]'),
    (LEADER_SKILL_APPLIES_SHINY, 'Idols of all 3 types [Shiny]'),
]

# To get leader skill name:
# If applies_to, concatenate suffix and prefix, otherwise, concatenate idol type and suffix

LEADER_SKILL_NAME_PREFIX = {
    LEADER_SKILL_APPLIES_TRICOLOR: _('Tricolor'),
    LEADER_SKILL_APPLIES_SHINY: _('Shiny'),
}

JAPANESE_LEADER_SKILL_NAME_PREFIX = {
    LEADER_SKILL_APPLIES_TRICOLOR: u'トリコロール・',
    LEADER_SKILL_APPLIES_SHINY: u'シャイニー',
}

LEADER_SKILLS_WITHOUT_PREFIX = [
    LEADER_SKILL_CINDERELLA_CHARM,
    LEADER_SKILL_FORTUNE_PRESENT,
]

LEADER_SKILL_NAME_SUFFIX = {
    STAT_VOCAL: _('Voice'),
    STAT_VISUAL: _('Make-Up'),
    STAT_DANCE: _('Step'),
    LEADER_SKILL_BRILLIANCE: _('Brilliance'),
    LEADER_SKILL_PRINCESS: _('Princess'),
    LEADER_SKILL_ABILITY: _('Ability'),
    LEADER_SKILL_ENERGY: _('Energy'),
    LEADER_SKILL_CHEER: _('Cheer'),
    LEADER_SKILL_CINDERELLA_CHARM: _('Cinderella Charm'),
    LEADER_SKILL_FORTUNE_PRESENT: _('Fortune Present'),
}

JAPANESE_LEADER_SKILL_NAME_SUFFIX = {
    STAT_VOCAL: u'ボイス',
    STAT_VISUAL: u'メイク',
    STAT_DANCE: u'ステップ',
    LEADER_SKILL_BRILLIANCE: u'ブリリアンス',
    LEADER_SKILL_PRINCESS: u'プリンセス',
    LEADER_SKILL_ABILITY: u'アビリティ',
    LEADER_SKILL_ENERGY: u'エナジー',
    LEADER_SKILL_CHEER: u'チアー',
    LEADER_SKILL_CINDERELLA_CHARM: u'シンデレラチャーム',
    LEADER_SKILL_FORTUNE_PRESENT: u'フォーチュンプレゼント',
}

# To get sentence template:
# Try applies_to then try type then default to LEADER_SKILL_BASE_SENTENCE

LEADER_SKILL_BASE_SENTENCE = _('Raises {leader_skill_type} of all {idol_type} idols by {leader_skill_percent}%.')
JAPANESE_LEADER_SKILL_BASE_SENTENCE = u'{idol_type}の{leader_skill_type}{leader_skill_percent}％アップ'

LEADER_SKILL_ONLY_TYPE_SENTENCE = _('Raises {leader_skill_type} of all {idol_type} idols by {leader_skill_percent}% when there are only {idol_type} idols on the team.')
JAPANESE_LEADER_SKILL_ONLY_TYPE_SENTENCE = u'{idol_type}アイドルのみ編成時、{idol_type}の{leader_skill_type}{leader_skill_percent}％アップ'

LEADER_SKILL_ALL_TYPES_SENTENCE = _('Raises {leader_skill_type} of all {idol_type} idols by {leader_skill_percent}% when there are {all_types} idols on the team.')
JAPANESE_LEADER_SKILL_ALL_TYPES_SENTENCE = u'3タイプ全てのアイドル編成時、{idol_type}の{leader_skill_type}{leader_skill_percent}％アップ'

LEADER_SKILL_SENTENCES_PER_APPLIES_TO = {
    LEADER_SKILL_APPLIES_TRICOLOR: LEADER_SKILL_ALL_TYPES_SENTENCE,
    LEADER_SKILL_APPLIES_SHINY: LEADER_SKILL_BASE_SENTENCE,
}

LEADER_SKILL_SENTENCES_PER_SKILL = {
    LEADER_SKILL_PRINCESS: LEADER_SKILL_ONLY_TYPE_SENTENCE,
    LEADER_SKILL_CHEER: LEADER_SKILL_ONLY_TYPE_SENTENCE,

    LEADER_SKILL_CINDERELLA_CHARM: _(u'Increases fan gain by {leader_skill_percent}% when you finish a live.'),
    LEADER_SKILL_FORTUNE_PRESENT: _(u'Gives extra rewards when you finish a live.'),
}

JAPANESE_LEADER_SKILL_SENTENCES_PER_APPLIES_TO = {
    LEADER_SKILL_APPLIES_TRICOLOR: JAPANESE_LEADER_SKILL_ALL_TYPES_SENTENCE,
    LEADER_SKILL_APPLIES_SHINY: JAPANESE_LEADER_SKILL_BASE_SENTENCE,
}

JAPANESE_LEADER_SKILL_SENTENCES_PER_SKILL = {
    LEADER_SKILL_PRINCESS: JAPANESE_LEADER_SKILL_ONLY_TYPE_SENTENCE,
    LEADER_SKILL_CHEER: JAPANESE_LEADER_SKILL_ONLY_TYPE_SENTENCE,

    LEADER_SKILL_CINDERELLA_CHARM: u'LIVEクリア時、獲得ファン数が{leader_skill_percent}アップ',
    LEADER_SKILL_FORTUNE_PRESENT: u'LIVEクリア時、特別報酬を追加で獲得',
}

_ALL_APPEALS = lambda: _('{type} appeal').format(type=u'/'.join([
    unicode(t[1]) for t in TYPE_CHOICES
]))

LEADER_SKILL_RAISED_STAT = {
    STAT_VOCAL: lambda: _('{type} appeal').format(type=unicode(_('Vocal'))),
    STAT_VISUAL: lambda: _('{type} appeal').format(type=unicode(_('Visual'))),
    STAT_DANCE: lambda: _('{type} appeal').format(type=unicode(_('Dance'))),
    LEADER_SKILL_BRILLIANCE: _ALL_APPEALS,
    LEADER_SKILL_PRINCESS: _ALL_APPEALS,
    LEADER_SKILL_ABILITY: lambda: _('Skill probability'),
    LEADER_SKILL_ENERGY: lambda: _('Life'),
    LEADER_SKILL_CHEER: lambda: _('Life'),
    LEADER_SKILL_CINDERELLA_CHARM: lambda: '',
    LEADER_SKILL_FORTUNE_PRESENT: lambda: '',
}

JAPANESE_LEADER_SKILL_RAISED_STAT = {
    STAT_VOCAL: u'ボーカルアピール値',
    STAT_VISUAL: u'ビジュアルアピール値',
    STAT_DANCE: u'ダンスアピール値',
    LEADER_SKILL_BRILLIANCE: u'全アピール値',
    LEADER_SKILL_PRINCESS: u'全アピール値',
    LEADER_SKILL_ABILITY: u'特技発動確率',
    LEADER_SKILL_ENERGY: u'ライフ',
    LEADER_SKILL_CHEER: u'ライフ',
    LEADER_SKILL_CINDERELLA_CHARM: '',
    LEADER_SKILL_FORTUNE_PRESENT: '',
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
PLAY_WITH_CHOICES = [ (index, localized) for (index, (localized, _name)) in enumerate(PLAY_WITH) ]
PLAY_WITH_DICT = dict(PLAY_WITH_CHOICES)
PLAY_WITH_ICONS = dict([ (index, icon) for (index, (_name, icon)) in enumerate(PLAY_WITH) ])

OS = [ 'iOs', 'Android' ]
OS_CHOICES = list(enumerate(OS))
OS_DICT = dict(OS_CHOICES)

PRODUCER_RANK = [
    'E', 'D', 'C', 'B', 'A', 'S', 'SS'
]
PRODUCER_RANK_CHOICES = list(enumerate(PRODUCER_RANK))
PRODUCER_RANK_DICT = dict(PRODUCER_RANK_CHOICES)
