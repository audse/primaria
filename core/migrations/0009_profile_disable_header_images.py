# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-04-18 23:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20180416_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='disable_header_images',
            field=models.BooleanField(default=False),
        ),
    ]
