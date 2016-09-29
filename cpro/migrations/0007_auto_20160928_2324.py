# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0006_auto_20160928_2259'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favoritecard',
            unique_together=set([('account', 'card')]),
        ),
    ]
