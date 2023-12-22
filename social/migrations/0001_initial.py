# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2023-12-22 19:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Badge",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rank", models.CharField(max_length=140)),
                ("area", models.CharField(max_length=140)),
                ("awarded", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Board",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=140)),
                ("url", models.CharField(max_length=140)),
                ("description", models.TextField()),
                ("staff", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("subject", models.CharField(blank=True, max_length=140, null=True)),
                ("text", models.TextField(blank=True, null=True)),
                ("read", models.BooleanField(default=False)),
                ("deleted_by_sender", models.BooleanField(default=False)),
                ("deleted_by_receiver", models.BooleanField(default=False)),
                (
                    "original_message",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="original",
                        to="social.Message",
                    ),
                ),
                (
                    "receiving_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="receiving_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sending_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sending_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reply",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField()),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("deleted", models.BooleanField(default=False)),
                (
                    "deleted_reason",
                    models.CharField(blank=True, max_length=140, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=140)),
                ("slug", models.SlugField(blank=True)),
                ("message", models.TextField()),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "last_reply_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("deleted", models.BooleanField(default=False)),
                ("locked", models.BooleanField(default=False)),
                ("sticky", models.BooleanField(default=False)),
                (
                    "board",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="social.Board",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="reply",
            name="topic",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="social.Topic",
            ),
        ),
        migrations.AddField(
            model_name="reply",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
