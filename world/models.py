from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from shop.models import Item


class Score(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    game = models.CharField(max_length=140)
    date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username + "'s " + self.game + " score"


class DailyClaim(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    daily_type = models.CharField(max_length=140)
    message = models.CharField(max_length=1024)
    reward = models.ForeignKey(
        "shop.Item", blank=True, null=True, on_delete=models.CASCADE
    )
    points = models.IntegerField(blank=True, null=True)
    date_of_claim = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username + "'s " + self.daily_type + " claim"


class MedicinePickup(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    cost = models.IntegerField(default=250)
    item = models.ForeignKey(
        "shop.Item", blank=True, null=True, on_delete=models.CASCADE
    )
