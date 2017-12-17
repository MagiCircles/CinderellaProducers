# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0015_auto_20170217_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='i_skill',
            field=models.PositiveIntegerField(null=True, verbose_name='Skill', choices=[(0, 'Lesser Perfect Lock'), (1, 'Greater Perfect Lock'), (2, 'Extreme Perfect Lock'), (3, 'Combo Lock'), (4, 'Healer'), (5, 'Life Lock'), (6, 'Combo Bonus'), (7, 'Perfect Score Bonus'), (8, 'Overload'), (9, 'Score Boost'), (10, 'All Round'), (11, 'Concentration'), (12, 'Skill Boost'), (13, 'Cute/Cool/Passion Focus')]),
            preserve_default=True,
        ),
    ]
