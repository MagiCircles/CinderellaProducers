# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cpro.models


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0014_auto_20170129_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='art_hd_awakened',
            field=models.ImageField(upload_to=cpro.models.uploadItem(b'c/art_hd/a'), null=True, verbose_name='Art (HD Awakened)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_skill',
            field=models.PositiveIntegerField(null=True, verbose_name='Skill', choices=[(0, 'Lesser Perfect Lock'), (1, 'Greater Perfect Lock'), (2, 'Extreme Perfect Lock'), (3, 'Combo Lock'), (4, 'Healer'), (5, 'Life Lock'), (6, 'Combo Bonus'), (7, 'Perfect Score Bonus'), (8, 'Overload'), (9, 'Score Boost'), (10, 'All Round'), (11, 'Concentration')]),
            preserve_default=True,
        ),
    ]
