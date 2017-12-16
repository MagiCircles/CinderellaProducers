# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cpro.models


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0013_auto_20161025_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='art_hd',
            field=models.ImageField(upload_to=cpro.models.uploadItem(b'c/art_hd'), null=True, verbose_name='Art (HD)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='art_hd_awakened',
            field=models.ImageField(upload_to=cpro.models.uploadItem(b'c/art_hd/a'), null=True, verbose_name='Art_Hd (Awakened)'),
            preserve_default=True,
        ),
    ]
