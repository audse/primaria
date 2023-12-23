from django.shortcuts import render, redirect
import random
from shop.models import Item, Category, Inventory
from social.models import Message
from core.models import Avatar
from utils.error import error_page
from shop.views.shop import shop_page
from goddess.views import goddess_commerce_page


def restricted_area_page(request):
    if request.user.is_authenticated:
        mystery_card = Item.objects.get(url="mystery-card")
        mystery_card = Inventory.objects.filter(
            user=request.user, item=mystery_card, box=False, pending=False
        ).first()
        activated_card = Item.objects.get(url="activated-area-card")
        activated_card = Inventory.objects.filter(
            user=request.user, item=activated_card, box=False, pending=False
        ).first()

        inventory = Inventory.objects.filter(
            user=request.user,
            box=False,
            pending=False,
            item__category=Category.objects.get(name="crystal"),
        )
        results = request.session.pop("results", False)
        return render(
            request,
            "world/restricted_area_page.html",
            {
                "mystery_card": mystery_card,
                "activated_card": activated_card,
                "inventory": inventory,
                "results": results,
            },
        )
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def update_card(request, crystal):
    if request.user.is_authenticated:
        mystery_card = Item.objects.get(url="mystery-card")
        mystery_card = Inventory.objects.filter(
            user=request.user, item=mystery_card
        ).first()
        if mystery_card is not None:
            if (
                crystal == "amethyst"
                or crystal == "aquamarine"
                or crystal == "diamond"
                or crystal == "emerald"
                or crystal == "ruby"
                or crystal == "sapphire"
                or crystal == "topaz"
            ):
                crystal_item = Item.objects.get(url="big-" + crystal + "-crystal-piece")
                inventory = Inventory.objects.filter(
                    item=crystal_item, user=request.user, box=False, pending=False
                ).first()
                if inventory is not None:
                    inventory.delete()
                    new_card = Item.objects.get(url="deactivated-bank-card")
                    mystery_card.item = new_card
                    mystery_card.save()
                    return redirect(shop_page, "alchemist")
                else:
                    request.session["error"] = "You do not have that crystal to give."
                    return redirect(error_page)
            else:
                request.session["error"] = "That crystal does not exist."
                return redirect(error_page)
        else:
            request.session["error"] = "You must have a Mystery Card to view this page."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def activate_card(request):
    if request.user.is_authenticated:
        deactivated_card = Item.objects.get(url="deactivated-bank-card")
        deactivated_card = Inventory.objects.filter(
            item=deactivated_card, user=request.user, box=False, pending=False
        ).first()
        if deactivated_card is not None:
            if request.user.profile.points >= 1000:
                request.user.profile.subtract_points(1000)
                new_card = Item.objects.get(url="activated-area-card")
                deactivated_card.item = new_card
                deactivated_card.save()
                return redirect(goddess_commerce_page)
            else:
                request.session[
                    "error"
                ] = "You do not have enough points to activate your card."
                return redirect(error_page)
        else:
            request.session[
                "error"
            ] = 'You must have a Deactivated "Bank Card" to view this page.'
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def restricted_machine(request):
    if request.user.is_authenticated:
        activated_card = Item.objects.get(url="activated-area-card")
        activated_card = Inventory.objects.filter(
            user=request.user, item=activated_card, box=False, pending=False
        ).first()
        if activated_card != None:
            items = request.POST.get("items")
            if items:
                items = items.split(",")
                crystals = []
                for item in items:
                    item = int(item)
                    item = Inventory.objects.filter(
                        item__category=Category.objects.get(name="crystal"),
                        user=request.user,
                        box=False,
                        pending=False,
                        pk=item,
                    ).first()
                    if item is None:
                        request.session["error"] = "All items must be your own."
                        return redirect(error_page)
                    crystals.append(item)
                if len(crystals) <= 3:
                    total_value = 0
                    for crystal in crystals:
                        if "big" in crystal.item.name.lower():
                            total_value += 5
                        else:
                            total_value += 1
                        if "diamond" in crystal.item.name.lower():
                            total_value += 4

                    rarity = 0
                    # possible: 3, 7, 11, 15
                    if total_value <= 3:  # low chance of rare
                        random_rarity = random.randint(1, 50)
                        if random_rarity < 10:
                            rarity = 0
                        elif random_rarity < 41:
                            rarity = 1
                        elif random_rarity < 50:
                            rarity = 2
                        else:
                            rarity = 3
                    elif total_value <= 7:
                        random_rarity = random.randint(1, 40)
                        if random_rarity < 3:
                            rarity = 0
                        elif random_rarity < 25:
                            rarity = 1
                        elif random_rarity < 35:
                            rarity = 2
                        elif random_rarity < 40:
                            rarity = 3
                        else:
                            rarity = 4
                    elif total_value <= 11:
                        random_rarity = random.randint(1, 40)
                        if random_rarity == 1:
                            rarity = 0
                        elif random_rarity < 15:
                            rarity = 1
                        elif random_rarity < 25:
                            rarity = 2
                        elif random_rarity < 39:
                            rarity = 3
                        else:
                            rarity = 4

                    elif total_value <= 15:
                        random_rarity = random.randint(1, 40)
                        if random_rarity == 1:
                            rarity = 0
                        elif random_rarity < 10:
                            rarity = 1
                        elif random_rarity < 20:
                            rarity = 2
                        elif random_rarity < 30:
                            rarity = 3
                        else:
                            rarity = 4

                    potion_category = Category.objects.get(name="potion")
                    reward = (
                        Item.objects.filter(category=potion_category, rarity=rarity)
                        .order_by("?")
                        .first()
                    )
                    inventory = Inventory.objects.create(user=request.user, item=reward)
                    for crystal in crystals:
                        crystal.delete()

                    # AVATARS
                    if random.randint(1, 4) == 1:
                        rulebreaker_avatar = Avatar.objects.get(url="rulebreaker")
                        if rulebreaker_avatar not in request.user.profile.avatars.all():
                            request.user.profile.avatars.add(rulebreaker_avatar)
                            request.user.profile.save()
                            message = Message.objects.create(
                                receiving_user=request.user,
                                subject="You just found a secret avatar!",
                                text='You have just received the avatar "Rulebreaker!" to use on the boards!',
                            )

                    request.session["results"] = (
                        "You have used your crystals and obtained a new "
                        + reward.name
                        + "!"
                    )
                    return redirect(restricted_area_page)

                else:
                    request.session[
                        "error"
                    ] = "You cannot use more than three crystals."
                    return redirect(error_page)
            else:
                request.session["error"] = "You must use at least one crystal."
                return redirect(error_page)
        else:
            request.session[
                "error"
            ] = "You must have an Activated Area Card to view this page."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)
