# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-04-21 22:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_auto_20180419_1829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='collectible',
        ),
        migrations.AddField(
            model_name='item',
            name='usable',
            field=models.BooleanField(default=True),
        ),
    ]
