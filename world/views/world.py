from django.shortcuts import render, redirect

from datetime import datetime

from ..models import DailyClaim
from shop.models import Shop, Item, Inventory
from utils.error import error_page


def world_page(request):
    city_shops = Shop.objects.filter(location="city").order_by("name")
    suburb_shops = Shop.objects.filter(location="suburbs").order_by("name")
    reservoir_shops = Shop.objects.filter(location="reservoir").order_by("name")
    caves_shops = Shop.objects.filter(location="caves").order_by("name")
    beach_shops = Shop.objects.filter(location="beach").order_by("name")
    return render(
        request,
        "world/world_page.html",
        {
            "city_shops": city_shops,
            "suburb_shops": suburb_shops,
            "reservoir_shops": reservoir_shops,
            "caves_shops": caves_shops,
            "beach_shops": beach_shops,
        },
    )


def dump_page(request):
    success = request.session.pop("success", False)
    dump_items = Inventory.objects.filter(user=None).order_by("?")[:18]
    if request.user.is_authenticated():
        inventory = Inventory.objects.filter(
            user=request.user, box=False, pending=False
        )
    else:
        inventory = None
    return render(
        request,
        "world/dump_page.html",
        {"dump_items": dump_items, "success": success, "inventory": inventory},
    )


def take_from_dump(request, pk):
    if request.user.is_authenticated():
        item = Inventory.objects.filter(user=None, pk=pk).first()
        if item:
            item.user = request.user
            item.save()
            request.session["success"] = (
                "You have successfully taken the " + item.item.name + " from the dump!"
            )
            return redirect(dump_page)
        else:
            request.session["error"] = "That item does not exist."
            return redirect(error_page)

    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def dump_item(request):
    if request.user.is_authenticated():
        pk = request.POST.get("item")
        try:
            pk = int(pk)
        except:
            request.session["error"] = "That item does not exist."
            return redirect(error_page)
        item = Inventory.objects.filter(user=request.user, pk=pk).first()
        if item:
            item.user = None
            item.save()
            request.session["success"] = (
                "You have added " + item.item.name + " to the dump..."
            )
            return redirect(dump_page)
        else:
            request.session["error"] = "That item does not exist."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def vending_machine_page(request):
    if request.user.is_authenticated():
        today = datetime.today()
        vend_claim = DailyClaim.objects.filter(
            user=request.user,
            daily_type="vend",
            date_of_claim__year=today.year,
            date_of_claim__month=today.month,
            date_of_claim__day=today.day,
            date_of_claim__hour=today.hour,
        ).first()
    else:
        vend_claim = None
    candies = Item.objects.filter(second_category__name="candy")
    return render(
        request,
        "world/daily/vending_machine_page.html",
        {"vend_claim": vend_claim, "candies": candies},
    )


def vending_machine(request, pk):
    if request.user.is_authenticated():
        today = datetime.today()
        vend_claim = DailyClaim.objects.filter(
            user=request.user,
            daily_type="vend",
            date_of_claim__year=today.year,
            date_of_claim__month=today.month,
            date_of_claim__day=today.day,
            date_of_claim__hour=today.hour,
        ).first()
        if vend_claim == None:
            item = Item.objects.filter(second_category__name="candy", pk=pk).first()
            if item is not None:
                if (
                    Inventory.objects.filter(
                        user=request.user, box=False, pending=False
                    ).count()
                    < 50
                ):
                    if request.user.profile.points >= 50:
                        request.user.profile.points -= 50
                        request.user.profile.save()
                        message = (
                            "You insert some coins and out pops a " + item.name + "."
                        )

                        inventory = Inventory.objects.create(
                            user=request.user, item=item
                        )
                        claim = DailyClaim.objects.create(
                            user=request.user,
                            daily_type="vend",
                            message=message,
                            reward=item,
                        )
                        return redirect(vending_machine_page)
                    else:
                        request.session[
                            "error"
                        ] = "You do not have enough points to use the Vending Machine."
                        return redirect(error_page)
                else:
                    request.session[
                        "error"
                    ] = "You can only have up to 50 items in your inventory."
                    return redirect(error_page)
            else:
                request.session["error"] = "That candy does not exist."
                return redirect(error_page)
        else:
            request.session["error"] = "You have already taken something this hour."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)
