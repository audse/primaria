from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.core.paginator import Paginator


from ..models import Item, Inventory, UserShop, UserShopStock

from utils.error import handle_error, require_login, error_page


def your_shop_page(request):
    if request.user.is_authenticated():
        shop = UserShop.objects.filter(user=request.user).first()
        user_items = Inventory.objects.filter(user=request.user, box=False, pending=False)
        if shop:
            shop_items = UserShopStock.objects.filter(shop=shop)
        else:
            shop_items = None
        return render(request, 'shop/your_shop_page.html', {'shop':shop, 'shop_items':shop_items, 'user_items':user_items})
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def open_shop_page(request):
    if request.user.is_authenticated():
        shop = UserShop.objects.filter(user=request.user).first()
        if shop == None:
            return render(request, 'shop/open_shop_page.html')
        else:
            request.session['error'] = "You have already created a shop."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def open_shop(request):
    if request.user.is_authenticated():
        shop = UserShop.objects.filter(user=request.user).first()
        if shop is None:
            if request.user.profile.points >= 500:
                request.user.profile.points -= 500
                request.user.profile.save()
                shop = UserShop.objects.create(user=request.user, name=request.POST.get("shop_name"))
                return redirect(your_shop_page)
            else:
                request.session['error'] = "You do not have enough points to open a shop."
                return redirect(error_page)
        else:
            request.session['error'] = "You have already created a shop."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def add_shop_item(request):
    if request.user.is_authenticated():
        shop = UserShop.objects.filter(user=request.user).first()
        if shop:
            item = request.POST.get("item")
            try:
                item = int(item)
            except:
                request.session['error'] = "That item does not exist."
                return redirect(error_page)

            inventory_item = Inventory.objects.filter(user=request.user, pk=item, box=False, pending=False).first()
            if inventory_item:
                
                item_count = UserShopStock.objects.filter(shop=shop).count()
                if item_count < shop.space:
                    price = request.POST.get("price")
                    try:
                        price = int(price)
                    except:
                        request.session['error'] = "Price must be an integer."
                        return redirect(error_page)
                    
                    new_shop_item = UserShopStock.objects.create(
                        item=inventory_item.item,
                        price=price,
                        shop=shop
                    )

                    inventory_item.delete()
                    return redirect(your_shop_page)
                else:
                    request.session['error'] = "Your shop is full right now."
                    return redirect(error_page)
            else:
                request.session['error'] = "That item does not exist."
                return redirect(error_page)
        else:
            request.session['error'] = "You do not yet have a shop."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def edit_price(request):
    if request.user.is_authenticated():
        shop = UserShop.objects.filter(user=request.user).first()
        if shop:
            price = request.POST.get("price")
            try:
                price = int(price)
            except:
                request.session['error'] = "Price must be an integer."
                return redirect(error_page)

            if shop.items:
                shop_item_pk = request.POST.get("item")
                shop_item = UserShopStock.objects.filter(pk=shop_item_pk).first()
                if shop_item:
                    shop_item.price = price
                    shop_item.save()
                    return redirect(your_shop_page)
                else:
                    request.session['error'] = "That item does not exist."
                    return redirect(error_page)
            else:
                request.session['error'] = "You have no items in your shop to edit."
                return redirect(error_page)
        else:
            request.session['error'] = "You do not yet have a shop."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def remove_from_shop(request):
    if request.user.is_authenticated():
        shop = UserShop.objects.filter(user=request.user).first()
        if shop:
            if shop.items:
                shop_item_pk = request.POST.get("item")
                shop_item = UserShopStock.objects.filter(pk=shop_item_pk).first()
                if shop_item:
                    
                    num_items_in_inventory = Inventory.objects.filter(
                            user=request.user,
                            box=False,
                            pending=False
                        ).count()
                    if num_items_in_inventory < 50:
                        inventory_item = Inventory.objects.create(
                                user=request.user,
                                item=shop_item.item
                            )
                        shop_item.delete()
                    else:
                        request.session['error'] = "You can only have up to 50 items in your inventory."
                        return redirect(error_page)

                    return redirect(your_shop_page)
                else:
                    request.session['error'] = "That item does not exist."
                    return redirect(error_page)
            else:
                request.session['error'] = "You have no items in your shop to edit."
                return redirect(error_page)
        else:
            request.session['error'] = "You do not yet have a shop."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def withdraw_shop_till(request):
    if request.user.is_authenticated():
        shop = UserShop.objects.filter(user=request.user).first()
        if shop:
            withdraw_amount = request.POST.get("withdraw_amount")
            try:
                withdraw_amount = int(withdraw_amount)
            except:
                request.session['error'] = "Withdraw amount must be an integer."
                return redirect(error_page)
            if withdraw_amount <= shop.shop_till:
                request.user.profile.points += withdraw_amount
                request.user.profile.save()
                shop.shop_till -= withdraw_amount
                shop.save()
                return redirect(your_shop_page)
            else:
                request.session['error'] = "You cannot withdraw more than you have in your shop till."
                return redirect(error_page)
        else:
            request.session['error'] = "You do not yet have a shop."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def upgrade_shop(request):
    if request.user.is_authenticated():
        shop = UserShop.objects.filter(user=request.user).first()
        if shop:
            if request.user.profile.points >= shop.upgrade_cost:
                request.user.profile.points -= shop.upgrade_cost
                request.user.profile.save()

                shop.space += 5
                shop.upgrade_cost = 100*shop.space
                shop.save()
                return redirect(your_shop_page)
            else:
                request.session['error'] = "You do not have enough points to upgrade your shop."
                return redirect(error_page)
        else:
            request.session['error'] = "You have not yet created a shop."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def user_shop_page(request, username):
    user = User.objects.filter(username=username).first()
    if user:
        shop = UserShop.objects.filter(user=user).first()
        if shop:
            shop_items = UserShopStock.objects.filter(shop=shop)
            return render(request, 'shop/user_shop_page.html', {'username':username, 'shop':shop, 'shop_items':shop_items})
        else:
            request.session['error'] = "That user does not yet have a shop."
            return redirect(error_page)
    else:
        request.session['error'] = "No user with that username ("+username+") was found."
        return redirect(error_page)

def purchase_from_user_shop(request, username):
    if request.user.is_authenticated():
        user = User.objects.filter(username=username).first()
        if user:
            shop = UserShop.objects.filter(user=user).first()

            if shop:
                shop_item_pk = request.POST.get("item_pk")
                shop_item = UserShopStock.objects.filter(pk=shop_item_pk).first()
                if shop_item:
                    
                    num_items_in_inventory = Inventory.objects.filter(
                            user=request.user,
                            box=False,
                            pending=False
                        ).count()

                    if num_items_in_inventory >= 50:
                        request.session['error'] = "You can only have up to 50 items in your inventory."
                        return redirect(error_page)
                    
                    if request.user.profile.points >= shop_item.price:
                        request.user.profile.points -= shop_item.price
                        request.user.profile.save()
                        inventory_item = Inventory.objects.create(
                                user=request.user,
                                item=shop_item.item
                            )
                        shop_item.delete()
                        shop.shop_till += shop_item.price
                        shop.save()

                    else:
                        request.session['error'] = "You do not have enough points to buy that item."
                        return redirect(error_page)

                    return redirect(user_shop_page, username=username)
                else:
                    request.session['error'] = "That item does not exist."
                    return redirect(error_page)
            else:
                request.session['error'] = "That user does not yet have a shop."
                return redirect(error_page)
        else:
            request.session['error'] = "No user with that username ("+username+") was found."
            return redirect(error_page)    
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def rename_shop(request):
    if request.user.is_authenticated():
        shop = UserShop.objects.filter(user=request.user).first()
        if shop:
            new_shop_name = request.POST.get("new_shop_name")
            shop.name = new_shop_name
            shop.save()
            return redirect(your_shop_page)
        else:
            request.session['error'] = "You have not yet created a shop."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)