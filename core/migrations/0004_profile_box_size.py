# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-04-14 22:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20180412_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='box_size',
            field=models.IntegerField(default=10),
        ),
    ]
