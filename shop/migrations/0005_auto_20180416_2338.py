# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2018-04-17 04:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20180414_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
