import datetime
import celery
from celery.task.schedules import crontab

from django.contrib.auth.models import User
from .models import Shop, Item, Category, BankAccount
from random import randint

# @celery.decorators.periodic_task(run_every=crontab(hour=13, minute=17))
@celery.decorators.periodic_task(run_every=datetime.timedelta(hours=1))
def restock():
	print("Restocking shops...")
	shops = Shop.objects.all()
	for shop in shops:
		shop.items.clear()
		items_in_category = Item.objects.filter(category=shop.category, rarity__lte=3) | Item.objects.filter(second_category=shop.category, rarity__lte=3)
		items_in_shop = items_in_category.order_by('?')[:18]
		for item in items_in_shop:
			shop.items.add(item)

		prices = []
		quantities = []

		for item in shop.items.all():
			if item.rarity == 1:
				quantities.append(randint(3, 10))
			elif item.rarity == 2:
				quantities.append(randint(1, 4))
			else:
				quantities.append(randint(1, 2))

			if item.price_class == 1:
				prices.append(randint(50,300))
			elif item.price_class == 2:
				prices.append(randint(300,800))
			elif item.price_class == 3:
				prices.append(randint(800,2000))
			elif item.price_class == 4:
				prices.append(randint(2000,4000))
			elif item.price_class == 5:
				prices.append(randint(4000,8000))
			elif item.price_class == 6:
				prices.append(randint(8000,12000))
			elif item.price_class == 7:
				prices.append(randint(12000,20000))
			elif item.price_class == 8:
				prices.append(randint(20000,30000))
			elif item.price_class == 9:
				prices.append(randint(50000,70000))
			elif item.price_class == 10:
				prices.append(randint(100000,150000))

		prices = ",".join(str(price) for price in prices)
		quantities = ",".join(str(quantity) for quantity in quantities)
		shop.prices = prices
		shop.quantities = quantities
		shop.save()

# def compound_interest(principal, rate, times_per_year, years):
#     # (1 + r/n)
#     body = 1 + (rate / times_per_year)
#     # nt
#     exponent = times_per_year * years
#     # P(1 + r/n)^nt
#     return principal * pow(body, exponent)

# @celery.decorators.periodic_task(run_every=datetime.timedelta(days=1))
# def set_interest():
# 	print("Setting interests...")
# 	all_interests = Interest.objects.all().delete()

# 	bank_accounts = BankAccount.objects.all()
# 	for account in bank_accounts:
# 		interest_amount = compound_interest(account.balance, 0.1, 365, 1)
# 		interest_amount = (interest_amount - account.balance) / 365
# 		interest = Interest.objects.create(user=account.user, amount=interest_amount)
