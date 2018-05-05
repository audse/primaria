from __future__ import unicode_literals

from django.db import models

from django.utils import timezone

from .unique_slugify import unique_slugify

class Message(models.Model):
	sending_user = models.ForeignKey('auth.User', related_name="sending_user", blank=True, null=True) # system messages
	receiving_user = models.ForeignKey('auth.User', related_name="receiving_user")
	original_message = models.ForeignKey('self', related_name="original", blank=True, null=True)
	
	date = models.DateTimeField(default=timezone.now)
	
	subject = models.CharField(max_length=140, blank=True, null=True)
	text = models.TextField(blank=True, null=True)

	read = models.BooleanField(default=False)
	deleted_by_sender = models.BooleanField(default=False)
	deleted_by_receiver = models.BooleanField(default=False)

	def __str__(self):
		if self.sending_user:
			return self.sending_user.username + "'s message to " + self.receiving_user.username
		else:
			return "System's message to " + self.receiving_user.username

class Badge(models.Model):
	user = models.ForeignKey('auth.User')
	rank = models.CharField(max_length=140) # Amateur, Professional, Expert
	area = models.CharField(max_length=140) # Plush Collector, Forum poster?
	awarded = models.DateTimeField(default=timezone.now)

class Board(models.Model):
	name = models.CharField(max_length=140)
	url = models.CharField(max_length=140)
	description = models.TextField()

	staff = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Topic(models.Model):
	user = models.ForeignKey('auth.User')
	board = models.ForeignKey('Board', blank=True, null=True)

	title = models.CharField(max_length=140)
	slug = models.SlugField(blank=True)
	message = models.TextField()
	date = models.DateTimeField(default=timezone.now)

	last_reply_date = models.DateTimeField(default=timezone.now)

	deleted = models.BooleanField(default=False)
	locked = models.BooleanField(default=False)
	sticky = models.BooleanField(default=False)

	def __str__(self):
		return self.title
	
	def save(self, **kwargs):
		slug_str = "%s %s" % (self.title, self.user.username) 
		unique_slugify(self, slug_str) 
		super(Topic, self).save(**kwargs)

class Reply(models.Model):
	user = models.ForeignKey('auth.User')
	topic = models.ForeignKey('Topic', blank=True, null=True)

	message = models.TextField()
	date = models.DateTimeField(default=timezone.now)

	deleted = models.BooleanField(default=False)
	deleted_reason = models.CharField(max_length=140, blank=True, null=True)

	def __str__(self):
		return self.user.username + "'s reply on \"" + self.topic.title + "\"" 






