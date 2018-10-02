# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0018_auto_20180912_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='_cache_owner_email',
            field=models.EmailField(max_length=75, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='level',
            field=models.PositiveIntegerField(null=True, verbose_name='Producer Level', validators=[django.core.validators.MaxValueValidator(500)]),
            preserve_default=True,
        ),
    ]
