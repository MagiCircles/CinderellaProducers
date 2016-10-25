# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0012_auto_20161021_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='level',
            field=models.PositiveIntegerField(null=True, verbose_name='Producer Level', validators=[django.core.validators.MaxValueValidator(300)]),
            preserve_default=True,
        ),
    ]
