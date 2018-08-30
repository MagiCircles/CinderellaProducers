# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0016_auto_20171216_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='leader_skill_apply',
            field=models.PositiveIntegerField(null=True, verbose_name=b'Leader Skill: Which idols does it apply to?', choices=[(None, b'Idols of the same type [Cute/Cool/Passion]'), (1, b'Idols of all 3 types, when all types are in the team [Tricolor]'), (2, b'Idols of all 3 types [Shiny]')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='skill_value3',
            field=models.FloatField(null=True, verbose_name=b'Other Skill Value'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_skill',
            field=models.PositiveIntegerField(null=True, verbose_name='Skill', choices=[(0, 'Lesser Perfect Lock'), (1, 'Greater Perfect Lock'), (2, 'Extreme Perfect Lock'), (3, 'Combo Lock'), (4, 'Healer'), (5, 'Life Lock'), (6, 'Combo Bonus'), (7, 'Perfect Score Bonus'), (8, 'Overload'), (9, 'Score Boost'), (10, 'All Round'), (11, 'Concentration'), (12, 'Skill Boost'), (13, 'Cute/Cool/Passion Focus'), (14, 'Encore'), (15, 'Sparkle'), (16, 'Tricolor Synergy')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='leader_skill_percent',
            field=models.FloatField(null=True, verbose_name=b'Leader Skill: Percentage'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='leader_skill_type',
            field=models.PositiveIntegerField(null=True, verbose_name=b'Leader Skill: What kind of stat gets raised?', choices=[(0, b'Vocal appeal [Voice]'), (2, b'Visual appeal [Make-up]'), (1, b'Dance appeal [Step]'), (101, b'Vocal/Visual/Dance appeals [Brilliance]'), (105, b'Vocal/Visual/Dance appeals, when only same type in the team [Princess]'), (103, b'Skill probability [Ability]'), (102, b'Life [Energy]'), (104, b'Life, when only same type in the team [Cheer]'), (106, b'Fan gain, end of live [Cinderella Charm]'), (107, b'Rewards, end of live [Fortune Present]')]),
            preserve_default=True,
        ),
    ]
