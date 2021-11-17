from django.shortcuts import render, redirect

from datetime import datetime
import random

from ..models import DailyClaim
from shop.models import Item, Category, Inventory
from social.models import Message
from core.models import Avatar
from utils.error import error_page

def fishing_page(request):
    if request.user.is_authenticated():
        today = datetime.today()
        fish_claim = DailyClaim.objects.filter(user=request.user, daily_type="fish", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day, date_of_claim__hour=today.hour).first()
        fish_category = Category.objects.get(name="fishing")
        inventory_fish = Inventory.objects.filter(user=request.user, item__category=fish_category, item__name__icontains="fish", box=False, pending=False)
        return render(request, 'world/fishing_page.html', {'fish_claim':fish_claim, 'inventory_fish':inventory_fish})
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def purchase_rod(request):
    if request.user.is_authenticated():
        if request.user.profile.points >= 5000:
            if request.user.profile.fishing_rod < 1:
                request.user.profile.subtract_points(5000)
                request.user.profile.fishing_rod = 1
                request.user.profile.save()
                return redirect(fishing_page)
            else:
                request.session['error'] = "You already have a fishing rod."
        else:
            request.session['error'] = "You do not have enough points to buy a Basic Rod."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def upgrade_rod(request):
    if request.user.is_authenticated():
        if request.user.profile.fishing_rod == 1:
            points = 10000
        elif request.user.profile.fishing_rod == 2:
            points = 25000
        else:
            request.session['error'] = "You must have a Rod to upgrade, and you cannot upgrade from a Best Rod."
            return redirect(error_page)

        if request.user.profile.points >= points:
            request.user.profile.subtract_points(points)
            request.user.profile.fishing_rod += 1
            request.user.profile.save()
            return redirect(fishing_page)
        else:
            request.session['error'] = "You do not have enough points to upgrade your rod."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def purchase_bait(request):
    if request.user.is_authenticated():
        amount = request.POST.get('amount')
        try:
            amount = int(amount)
        except:    
            request.session['error'] = "Amount must be an integer."
            return redirect(error_page)
        price = amount * 25
        if request.user.profile.points >= price:
            request.user.profile.subtract_points(price)
            request.user.profile.fishing_bait += amount
            request.user.profile.save()
            return redirect(fishing_page)
        else:
            request.session['error'] = "You do not have enough points to buy " + str(amount) + " bait."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def fish(request):
    if request.user.is_authenticated():
        today = datetime.today()
        fish_claim = DailyClaim.objects.filter(user=request.user, daily_type="fish", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day, date_of_claim__hour=today.hour).first()
        if fish_claim is None:
            if request.user.profile.fishing_bait > 0:
                if request.user.profile.fishing_rod > 0:
                    request.user.profile.fishing_bait -= 1
                    request.user.profile.save()
                    if request.user.profile.fishing_rod == 1: # basic rod
                        rarity_set = [None, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2]
                    elif request.user.profile.fishing_rod == 2: # better rod
                        rarity_set = [None, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2]
                    elif request.user.profile.fishing_rod == 3: # best rod
                        rarity_set = [None, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
                    rarity = random.choice(rarity_set)

                    fishing_skill_bonus = random.randint(request.user.profile.fishing_skill, 20)
                    if fishing_skill_bonus == 20:
                        if rarity < 3:
                            rarity += 1

                    fishing_category = Category.objects.filter(name="fishing")
                    if Inventory.objects.filter(user=request.user, box=False, pending=False).count() < 50:
                        if rarity is not None:
                            reward = Item.objects.filter(rarity=rarity, category=fishing_category).order_by('?').first()
                            
                            message = "You cast your line and... you pull up a " + reward.name + "!"
                            if rarity > 0: # rarity 0 is junk...boot, tire, etc
                                if request.user.profile.fishing_skill < 10:
                                    message += " Your fishing skill progress went up one point!"
                                    request.user.profile.fishing_skill_progress += 1
                                    if request.user.profile.fishing_skill_progress == 10*request.user.profile.fishing_skill:
                                        request.user.profile.fishing_skill += 1
                                        request.user.profile.fishing_skill_progress == 0
                                    request.user.profile.save()
                            claim = DailyClaim.objects.create(user=request.user, daily_type="fish", message=message, reward=reward)
                            inventory = Inventory.objects.create(user=request.user, item=reward)
                            
                            # AVATARS

                            rand_num = random.randint(1,5)
                            if rand_num == 1:
                                penguin_avatar = Avatar.objects.get(url="saved-a-penguin")
                                if penguin_avatar not in request.user.profile.avatars.all():
                                    if inventory.item.url == "six-pack-rings":
                                        request.user.profile.avatars.add(penguin_avatar)
                                        request.user.profile.save()
                                        message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Saved a Penguin\" to use on the boards!")

                            return redirect(fishing_page)
                        else:
                            message = "You cast your line and... you pull up... absolutely nothing! That's too bad, try again some other time!"
                            claim = DailyClaim.objects.create(user=request.user, daily_type="fish", message=message, reward=None)
                            return redirect(fishing_page)
                    else:
                        request.session['error'] = "You can only have up to 50 items in your inventory."
                        return redirect(error_page)
                else:
                    request.session['error'] = "You must have a rod to go fishing."
                    return redirect(error_page)
            else:
                request.session['error'] = "You must have at least one bait to go fishing."
                return redirect(error_page)
        else:
            request.session['error'] = "You have already fished this hour."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def sell_fish(request, pk):
    if request.user.is_authenticated():
        fishing_category = Category.objects.filter(name="fishing")
        fish = Inventory.objects.filter(user=request.user, pk=pk, item__category=fishing_category, item__name__icontains="fish").first()
        if fish:
            if fish.item.rarity == 1:
                price = 200
            elif fish.item.rarity == 2:
                price = 500
            elif fish.item.rarity == 3:
                price = 1000
            request.user.profile.points += price
            request.user.profile.save()
            fish.delete()
            return redirect(fishing_page)
        else:
            request.session['error'] = "That item does not exist."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)
