from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


class Quest(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    goddess = models.CharField(max_length=140)

    requested_item = models.ForeignKey(
        "shop.Item", related_name="requested_item", on_delete=models.CASCADE
    )
    completed = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)  # for avatar

    reward_item = models.ForeignKey(
        "shop.Item", blank=True, null=True, on_delete=models.CASCADE
    )
    reward_points = models.IntegerField(blank=True, null=True)

    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username + "'s quest from the Goddess of " + self.goddess
