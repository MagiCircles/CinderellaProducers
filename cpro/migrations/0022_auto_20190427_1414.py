# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0021_auto_20190427_0730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='_cache_event_last_update',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_idol_last_update',
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_j_center_card',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_leader_skill_apply',
            field=models.PositiveIntegerField(default=0, verbose_name=b'Leader Skill: Which idols does it apply to?', choices=[(None, b'Idols of the same type [Cute/Cool/Passion]'), (1, b'Idols of all 3 types, when all types are in the team [Tricolor]'), (2, b'Idols of all 3 types [Shiny]')]),
            preserve_default=False,
        ),
    ]
