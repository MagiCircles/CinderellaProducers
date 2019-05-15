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

STAT_VOCAL = 0
STAT_DANCE = 1
STAT_VISUAL = 2

STAT_CHOICES = [
    (STAT_VOCAL, _('Vocal')),
    (STAT_DANCE, _('Dance')),
    (STAT_VISUAL, _('Visual')),
]
STAT_DICT = dict(STAT_CHOICES)

############################################################
# Card

# LEADER SKILL

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
