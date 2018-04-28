from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=140)
    url = models.CharField(max_length=140)
    description = models.TextField()

    category = models.ForeignKey('Category', blank=True, null=True)
    second_category = models.ForeignKey('Category', related_name="second_category", blank=True, null=True)
    price_class = models.IntegerField()
    rarity = models.IntegerField(default=1) # 1 to 5, very common to very rare

    # from -3 to 3, determines how pet is affected from use of an item
    hunger = models.IntegerField(default=0)
    wellness = models.IntegerField(default=0)
    happiness = models.IntegerField(default=0)

    usable = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    user = models.ForeignKey('auth.User', blank=True, null=True)
    item = models.ForeignKey('Item', blank=True, null=True)

    gallery = models.BooleanField(default=False)
    box = models.BooleanField(default=False)
    pending = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return self.user.username + "'s " + self.item.name
        else:
            return "In the dump: " + self.item.name

class Shop(models.Model):
    name = models.CharField(max_length=140)
    url = models.CharField(max_length=30)
    description = models.TextField()
    location = models.CharField(max_length=140)

    category = models.ForeignKey('Category')
    items = models.ManyToManyField('Item', blank=True)
    prices = models.CharField(max_length=140, blank=True, null=True)
    quantities = models.CharField(max_length=140, blank=True, null=True)

    restock = models.IntegerField() # 24 = per hour, 1 = per day, etc

    def __str__(self):
        return self.name

class BankAccount(models.Model):
    user = models.ForeignKey('auth.User')
    level = models.IntegerField(default=1)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + "'s Account"

# class Interest(models.Model):
#     user = models.ForeignKey('auth.User')
#     amount = models.IntegerField(default=0)

class Gallery(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.CharField(max_length=140, blank=True, null=True)
    space = models.IntegerField(default=5)
    upgrade_cost = models.IntegerField(default=500)

    plush = models.ManyToManyField('Item', blank=True, related_name="plush")
    cards = models.ManyToManyField('Item', blank=True, related_name="cards")

    def __str__(self):
        return self.user.username + "'s Gallery"

class UserShop(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.CharField(max_length=140, blank=True, null=True)
    space = models.IntegerField(default=5)
    upgrade_cost = models.IntegerField(default=500)

    items = models.TextField(blank=True, null=True) # Format: item_url.price,item_url.price, etc 
    shop_till = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + "'s Shop"

class Trade(models.Model):
    original_trade = models.ForeignKey('self', related_name="original", blank=True, null=True)
    sending_user = models.ForeignKey('auth.User', related_name="trade_sending_user")
    items = models.ManyToManyField('Inventory', related_name="items", blank=True)

    message = models.CharField(max_length=140, blank=True, null=True)

    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.sending_user.username + "'s trade"









