# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-04-19 01:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatars',
            field=models.ManyToManyField(blank=True, to='core.Avatar'),
        ),
        migrations.AddField(
            model_name='profile',
            name='selected_avatar',
            field=models.IntegerField(default=7),
        ),
    ]
