# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='i_kind',
            field=models.PositiveIntegerField(default=0, choices=[(0, 'Token'), (1, 'Medley'), (2, 'Coop'), (3, 'Caravan')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Join Date'),
            preserve_default=True,
        ),
    ]
