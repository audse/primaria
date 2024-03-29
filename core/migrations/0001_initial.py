# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2023-12-22 19:21
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
            name="Animal",
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
                ("name", models.CharField(max_length=64)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Avatar",
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
                ("name", models.CharField(max_length=64)),
                ("url", models.CharField(max_length=64)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="FriendRequest",
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
                ("note", models.TextField(blank=True, null=True)),
                (
                    "receiving_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="receiving_friend_request",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sending_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sending_friend_request",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Pet",
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
                ("name", models.CharField(max_length=64)),
                ("color", models.CharField(max_length=10)),
                ("all_colors", models.TextField()),
                ("hunger", models.IntegerField(default=3)),
                ("wellness", models.IntegerField(default=5)),
                ("happiness", models.IntegerField(default=1)),
                ("adopt_date", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "animal",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.Animal",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
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
                ("points", models.IntegerField(default=1000)),
                ("bio", models.TextField(blank=True, null=True)),
                (
                    "last_online",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "warnings",
                    models.TextField(
                        blank=True,
                        help_text="Please note the date, time, and a short description of each infraction.",
                        null=True,
                    ),
                ),
                ("disable_friend_requests", models.BooleanField(default=False)),
                ("box_size", models.IntegerField(default=10)),
                (
                    "selected_avatar",
                    models.CharField(default="hi-im-new", max_length=140),
                ),
                ("disable_header_images", models.BooleanField(default=False)),
                ("night_mode", models.BooleanField(default=False)),
                ("fishing_rod", models.IntegerField(default=0)),
                ("fishing_bait", models.IntegerField(default=0)),
                ("fishing_skill", models.IntegerField(default=1)),
                ("fishing_skill_progress", models.IntegerField(default=0)),
                ("dowsing_rod", models.IntegerField(default=0)),
                ("avatars", models.ManyToManyField(blank=True, to="core.Avatar")),
                (
                    "blocked_users",
                    models.ManyToManyField(
                        blank=True,
                        related_name="blocked_users_profiles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "friends",
                    models.ManyToManyField(
                        blank=True,
                        related_name="friends_profiles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
