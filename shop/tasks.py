import datetime
import celery
from celery.task.schedules import crontab

from django.contrib.auth.models import User
from .models import Shop, Item, Stock, Category, BankAccount
from random import randint

@celery.decorators.periodic_task(run_every=datetime.timedelta(minutes=10))
def restock():
    print("Restocking shops...")
    shops = Shop.objects.all()

    for shop in shops:
        shop.items.clear()
        
        num_items = randint(5, 18)
        items_in_category = Item.objects.filter(category=shop.category, rarity__lte=3) | Item.objects.filter(second_category=shop.category, rarity__lte=3)
        items_in_shop = items_in_category.order_by('?')[:num_items]
        
        for item in items_in_shop:

            price_class_prices = {
                1: randint(50, 300),
                2: randint(300, 800),
                3: randint(800, 2000),
                4: randint(2000, 4000),
                5: randint(4000, 8000),
                6: randint(8000, 12000),
                7: randint(12000, 20000),
                8: randint(20000, 30000),
                9: randint(50000, 70000),
                10: randint(100000, 150000)
            }

            quantity = 1
            if item.rarity == 1:
                quantity = randint(1, 10)
            elif item.rarity == 2:
                quantity = randint(1, 4)
            else:
                quantity = randint(1, 2)

            price = price_class_prices[item.price_class]

            Stock.objects.create(
                shop=shop,
                item=item,
                quantity=quantity,
                price=price
            )