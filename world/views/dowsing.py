from django.shortcuts import render, redirect

from datetime import datetime
import random

from ..models import DailyClaim
from shop.models import Item, Category, Inventory
from utils.error import error_page

def quarry_page(request):
    if request.user.is_authenticated():
        today = datetime.today()
        crystal_claim = DailyClaim.objects.filter(user=request.user, daily_type="dowse", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day, date_of_claim__hour=today.hour).first()
        inventory = {"amethyst":Inventory.objects.filter(user=request.user, item__url="small-amethyst-crystal-piece", box=False, pending=False).count(),"aquamarine":Inventory.objects.filter(user=request.user, item__url="small-aquamarine-crystal-piece", box=False, pending=False).count(),"diamond":Inventory.objects.filter(user=request.user, item__url="small-diamond-crystal-piece", box=False, pending=False).count(),"emerald":Inventory.objects.filter(user=request.user, item__url="small-emerald-crystal-piece", box=False, pending=False).count(),"ruby":Inventory.objects.filter(user=request.user, item__url="small-ruby-crystal-piece", box=False, pending=False).count(),"sapphire":Inventory.objects.filter(user=request.user, item__url="small-sapphire-crystal-piece", box=False, pending=False).count(),"topaz":Inventory.objects.filter(user=request.user, item__url="small-topaz-crystal-piece", box=False, pending=False).count()}
        return render(request, 'world/quarry_page.html', {'crystal_claim':crystal_claim, 'inventory':inventory})
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def purchase_dowsing_rod(request):
    if request.user.is_authenticated():
        if request.user.profile.points >= 10000:
            if request.user.profile.dowsing_rod < 1:
                request.user.profile.subtract_points(10000)
                request.user.profile.dowsing_rod = 1
                request.user.profile.save()
                return redirect(quarry_page)
            else:
                request.session['error'] = "You already have a dowsing rod."
        else:
            request.session['error'] = "You do not have enough points to buy a Basic Rod."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)
    pass

def upgrade_dowsing_rod(request):
    if request.user.is_authenticated():
        if request.user.profile.dowsing_rod == 1:
            points = 20000
        elif request.user.profile.dowsing_rod == 2:
            points = 50000
        else:
            request.session['error'] = "You must have a Rod to upgrade, and you cannot upgrade from a Best Rod."
            return redirect(error_page)

        if request.user.profile.points >= points:
            request.user.profile.subtract_points(points)
            request.user.profile.dowsing_rod += 1
            request.user.profile.save()
            return redirect(quarry_page)
        else:
            request.session['error'] = "You do not have enough points to upgrade your rod."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def dowse(request):
    if request.user.is_authenticated():
        today = datetime.today()
        crystal_claim = DailyClaim.objects.filter(user=request.user, daily_type="dowse", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day, date_of_claim__hour=today.hour).first()
        if crystal_claim is None:
            if request.user.profile.dowsing_rod > 0:
                if request.user.profile.points >= 200:
                    request.user.profile.subtract_points(200)
                    request.user.profile.save()

                    if Inventory.objects.filter(user=request.user, box=False, pending=False).count() < 50:
                        get_card = random.randint(1, 100)
                        if get_card != 1:

                            if request.user.profile.dowsing_rod == 1:
                                rarities = [None, None, None, None, None, None, 1, 1, 1, 1]
                            elif request.user.profile.dowsing_rod == 2:
                                rarities = [None, None, None, None, 1, 1, 1, 1, 2, 2]
                            elif request.user.profile.dowsing_rod == 3:
                                rarities = [None, None, None, 1, 1, 1, 1, 2, 2, 3]

                            rarity = random.choice(rarities)
                            if rarity is not None:
                                crystal_category = Category.objects.get(name="crystal")
                                reward = Item.objects.filter(category=crystal_category, name__icontains="Small", rarity=rarity).order_by('?').first()
                                message = "You try to find a crystal...and you find... a " + reward.name + "!"
                                claim = DailyClaim.objects.create(user=request.user, daily_type="dowse", message=message, reward=reward)
                                inventory = Inventory.objects.create(user=request.user, item=reward)
                                return redirect(quarry_page)
                            else:
                                message = "You try to find a crystal...and you find... absolutely nothing! That's too bad, try again some other time!"
                                claim = DailyClaim.objects.create(user=request.user, daily_type="dowse", message=message, reward=None)
                                return redirect(quarry_page)
                        else:
                            reward = Item.objects.get(url="mystery-card")
                            message = "You try to find a crystal...and you find... a... " + reward.name + "? That's kind of weird, someone must have dropped it..."
                            claim = DailyClaim.objects.create(user=request.user, daily_type="dowse", message=message, reward=reward)
                            inventory = Inventory.objects.create(user=request.user, item=reward)
                            return redirect(quarry_page)
                    else:
                        request.session['error'] = "You can only have up to 50 items in your inventory."
                        return redirect(error_page)
                else:
                    request.session['error'] = "You do not have enough points to go dowsing."
                    return redirect(error_page)
            else:
                request.session['error'] = "You must have a rod to go dowsing."
                return redirect(error_page)
        else:
            request.session['error'] = "You have already dowsed this hour."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def trade_crystals(request, crystal):
    if request.user.is_authenticated():
        if crystal == "amethyst" or crystal == "aquamarine" or crystal == "diamond" or crystal == "emerald" or crystal == "ruby" or crystal == "sapphire" or crystal == "topaz":
            crystal_str = crystal
            crystal = Item.objects.get(url="small-"+crystal+"-crystal-piece")
            crystals_in_inventory = Inventory.objects.filter(user=request.user, item=crystal, box=False, pending=False)
            if crystals_in_inventory.count() >= 5:
                n = 0
                for crystal in crystals_in_inventory:
                    if n < 5:
                        crystal.delete()
                        n += 1
                    else:
                        break
                new_crystal = Item.objects.get(url="big-"+crystal_str+"-crystal-piece")
                item = Inventory.objects.create(user=request.user, item=new_crystal)
                return redirect(quarry_page)
            else:
                request.session['error'] = "You do not have enough crystals to trade them in."
                return redirect(error_page)
        else:
            request.session['error'] = "That crystal does not exist."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)
