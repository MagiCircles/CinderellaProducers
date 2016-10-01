# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0008_auto_20160928_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='level',
            field=models.PositiveIntegerField(null=True, verbose_name='Producer Level'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='i_kind',
            field=models.PositiveIntegerField(default=0, verbose_name='Kind', choices=[(0, 'Token'), (1, 'Medley'), (2, 'Coop'), (3, 'Caravan'), (4, 'LIVE Parade')]),
            preserve_default=True,
        ),
    ]
