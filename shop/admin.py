from django.contrib import admin

from .models import Category, Item, Inventory, Shop, Stock, BankAccount, Gallery, UserShop, Trade, UserShopStock

admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(Shop)
admin.site.register(Stock)
admin.site.register(BankAccount)
admin.site.register(Gallery)
admin.site.register(UserShop)
admin.site.register(UserShopStock)
admin.site.register(Trade)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'second_category')
    list_filter = ('category', 'second_category')
    search_fields = ['name', 'category__name', 'second_category__name']