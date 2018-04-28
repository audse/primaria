from django.contrib import admin

from .models import Category, Item, Inventory, Shop, BankAccount, Gallery, UserShop, Trade

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Inventory)
admin.site.register(Shop)
admin.site.register(BankAccount)
admin.site.register(Gallery)
admin.site.register(UserShop)
admin.site.register(Trade)
