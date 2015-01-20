# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lp', '0004_auto_20141213_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfig',
            name='sms_key',
            field=models.CharField(max_length=64, null=True, verbose_name='SMS.RU Key', blank=True),
            preserve_default=True,
        ),
    ]
