# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lp', '0006_auto_20150120_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='ip',
            field=models.GenericIPAddressField(blank=True, editable=False, null=True, verbose_name='IP'),
        ),
        migrations.AlterField(
            model_name='tarifforder',
            name='ip',
            field=models.GenericIPAddressField(blank=True, editable=False, null=True, verbose_name='IP'),
        ),
    ]
