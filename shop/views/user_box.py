from django.shortcuts import render, redirect
from ..models import Inventory
from utils.error import error_page


def safety_deposit_box_page(request):
    if request.user.is_authenticated:
        inventory_items = Inventory.objects.filter(
            user=request.user, box=False, pending=False
        )
        box_items = Inventory.objects.filter(user=request.user, box=True)
        return render(
            request,
            "shop/safety_deposit_box_page.html",
            {"box_items": box_items, "inventory_items": inventory_items},
        )
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def add_box_item(request):
    if request.user.is_authenticated:
        item = request.POST.get("item")
        item = Inventory.objects.filter(
            user=request.user, box=False, pending=False, pk=item
        ).first()
        if item:
            box_items = Inventory.objects.filter(user=request.user, box=True).count()
            if box_items < request.user.profile.box_size:
                item.box = True
                item.save()
                return redirect(safety_deposit_box_page)
            else:
                request.session[
                    "error"
                ] = "Your Safety Deposit Box is already full. Please remove something or upgrade to add more."
                return redirect(error_page)
        else:
            request.session["error"] = "No item with that index exists."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def remove_box_item(request, item):
    if request.user.is_authenticated:
        item = Inventory.objects.filter(user=request.user, pk=item).first()
        if item:
            inventory_items = Inventory.objects.filter(
                user=request.user, box=False, pending=False
            ).count()
            if inventory_items < 50:
                item.box = False
                item.save()
                return redirect(safety_deposit_box_page)
            else:
                request.session[
                    "error"
                ] = "You can only have up to 50 items in your inventory."
                return redirect(error_page)
        else:
            request.session["error"] = "No item with that index exists."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def upgrade_box(request):
    if request.user.is_authenticated:
        if request.user.profile.points >= 1000:
            request.user.profile.subtract_points(1000)
            request.user.profile.box_size += 5
            request.user.profile.save()
            return redirect(safety_deposit_box_page)
        else:
            request.session[
                "error"
            ] = "You do not have enough points to upgrade your Safety Deposit Box."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)
