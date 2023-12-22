from django.shortcuts import render, redirect
from ..models import Item, Inventory, Shop, Stock, UserShopStock
from itertools import chain
from utils import avatars
from utils.error import handle_error, require_login, error_page


def shop_page(request, shop_url):
    shop = Shop.objects.get(url=shop_url)
    shop_items = Stock.objects.filter(shop=shop)

    # QUEST
    if shop.name == "Alchemist":
        inventory = {
            "amethyst": Inventory.objects.filter(
                user=request.user,
                item__url="big-amethyst-crystal-piece",
                box=False,
                pending=False,
            ).count(),
            "aquamarine": Inventory.objects.filter(
                user=request.user,
                item__url="big-aquamarine-crystal-piece",
                box=False,
                pending=False,
            ).count(),
            "diamond": Inventory.objects.filter(
                user=request.user,
                item__url="big-diamond-crystal-piece",
                box=False,
                pending=False,
            ).count(),
            "emerald": Inventory.objects.filter(
                user=request.user,
                item__url="big-emerald-crystal-piece",
                box=False,
                pending=False,
            ).count(),
            "ruby": Inventory.objects.filter(
                user=request.user,
                item__url="big-ruby-crystal-piece",
                box=False,
                pending=False,
            ).count(),
            "sapphire": Inventory.objects.filter(
                user=request.user,
                item__url="big-sapphire-crystal-piece",
                box=False,
                pending=False,
            ).count(),
            "topaz": Inventory.objects.filter(
                user=request.user,
                item__url="big-topaz-crystal-piece",
                box=False,
                pending=False,
            ).count(),
        }
        mystery_card = Item.objects.get(url="mystery-card")
        mystery_card = Inventory.objects.filter(
            user=request.user, item=mystery_card
        ).first()
        bank_card = Item.objects.get(url="deactivated-bank-card")
        bank_card = Inventory.objects.filter(user=request.user, item=bank_card).first()
    else:
        inventory = None
        mystery_card = None
        bank_card = None

    return render(
        request,
        "shop/shop_page.html",
        {
            "shop": shop,
            "shop_items": shop_items,
            "mystery_card": mystery_card,
            "inventory": inventory,
            "bank_card": bank_card,
        },
    )


def purchase_item(request, shop_url):
    require_login(request)

    item_pk = request.POST.get("item")

    shop = Shop.objects.get(url=shop_url)
    item = Stock.objects.get(pk=item_pk, shop=shop)

    points = request.user.profile.points
    num_items_in_inventory = Inventory.objects.filter(
        user=request.user, box=False, pending=False
    ).count()

    if not item:
        return handle_error(request, "Sorry, that item is not available at this time.")

    elif num_items_in_inventory >= 50:
        return handle_error(
            request, "You can only have up to 50 items in your inventory."
        )

    elif item.price >= points:
        return handle_error(request, "You do not have enough points to buy that item.")

    else:
        request.user.profile.subtract_points(item.price)
        inventory = Inventory.objects.create(user=request.user, item=item.item)

        # AVATARS
        avatars.get_yay_pink(request, inventory_item=inventory)

        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

    return redirect(shop_page, shop_url)


def shop_search_results_page(request):
    keyword = request.POST.get("keyword")
    if keyword is not None and keyword != "":
        new_keyword = keyword.replace(" ", "-").lower()

        shop_search_results = Stock.objects.filter(item__url__contains=new_keyword)
        user_search_results = UserShopStock.objects.filter(
            item__url__contains=new_keyword
        ).order_by("?")[:10]

        search_results = sorted(
            chain(shop_search_results, user_search_results), key=lambda o: o.price
        )

        return render(
            request,
            "shop/shop_search_results_page.html",
            {"keyword": keyword, "search_results": search_results},
        )
    else:
        request.session["error"] = "You must type a keyword to search."
        return redirect(error_page)
