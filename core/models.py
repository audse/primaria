from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField('auth.User', blank=True, null=True, on_delete=models.CASCADE)
    points = models.IntegerField(default=1000)
    bio = models.TextField(blank=True, null=True)
    last_online = models.DateTimeField(default=timezone.now)

    warnings = models.TextField(blank=True, null=True, help_text="Please note the date, time, and a short description of each infraction.")
    blocked_users = models.ManyToManyField('auth.User', blank=True, related_name="blocked_users")

    box_size = models.IntegerField(default=10)

    avatars = models.ManyToManyField('Avatar', blank=True)
    selected_avatar = models.CharField(max_length=140, default="hi-im-new")

    # SETTINGS
    disable_header_images = models.BooleanField(default=False)
    night_mode = models.BooleanField(default=False)

    # WORLD
    fishing_rod = models.IntegerField(default=0) # none=0, basic=1, etc
    fishing_bait = models.IntegerField(default=0)
    fishing_skill = models.IntegerField(default=1)
    fishing_skill_progress = models.IntegerField(default=0)

    dowsing_rod = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def subtract_points(self, amount):
        self.points -= amount
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Animal(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name

class Pet(models.Model):
    user = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.CASCADE) # pound
    name = models.CharField(max_length=64)
    color = models.CharField(max_length=10)
    animal = models.ForeignKey('Animal', blank=True, null=True, on_delete=models.CASCADE)

    all_colors = models.TextField()

    hunger = models.IntegerField(default=3)
    wellness = models.IntegerField(default=5)
    happiness = models.IntegerField(default=1)

    adopt_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.user:
            return self.user.username + "'s pet " + self.name
        else:
            return "Unadopted pet " + self.name

class Avatar(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name
