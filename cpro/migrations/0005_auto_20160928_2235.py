# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0004_auto_20160924_0213'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='art_awakened_on_homepage',
            field=models.BooleanField(default=True, help_text=b'Uncheck this if the awakened art looks weird because the idol is not in the center', verbose_name=b'Show the awakened art on the homepage of the site?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='art_on_homepage',
            field=models.BooleanField(default=True, help_text=b'Uncheck this if the art looks weird because the idol is not in the center', verbose_name=b'Show the art on the homepage of the site?'),
            preserve_default=True,
        ),
    ]
