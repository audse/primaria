from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from shop.models import Item

class Quest(models.Model):
	user = models.ForeignKey('auth.User')
	goddess = models.CharField(max_length=140)

	requested_item = models.ForeignKey('shop.Item', related_name="requested_item")
	completed = models.BooleanField(default=False)
	cancelled = models.BooleanField(default=False) # for avatar

	reward_item = models.ForeignKey('shop.Item', blank=True, null=True)
	reward_points = models.IntegerField(blank=True, null=True)

	date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.username + "'s quest from the Goddess of " + self.goddess
