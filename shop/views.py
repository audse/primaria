from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Category, Item, Inventory, Shop, Stock, BankAccount, Gallery, UserShop, Trade
from social.models import Message, Badge
from world.models import DailyClaim
from core.models import Animal, Pet, Avatar
from core.views import error_page

from operator import itemgetter
import random
from datetime import datetime

from utils.error import handle_error, require_login

def inventory_page(request):
    if request.user.is_authenticated():
        items = Inventory.objects.filter(user=request.user, box=False, pending=False)
        item_count = items.count()

        # AVATARS

        feeling_blue_avatar = Avatar.objects.get(url="feeling-blue")
        if feeling_blue_avatar not in request.user.profile.avatars.all():
            pet = Pet.objects.filter(user=request.user).first()
            if pet is not None:
                if pet.color == "blue" or pet.color == "blue-knit":
                    blue_items = 0
                    for item in items:
                        if "blue" in item.item.name.lower():
                            blue_items += 1
                    if blue_items >= 5:
                        request.user.profile.avatars.add(feeling_blue_avatar)
                        request.user.profile.save()
                        message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Feeling Blue...\" to use on the boards!")

        results = request.session.pop('results', False)
        return render(request, 'shop/inventory_page.html', {'items':items, 'item_count': item_count, 'results':results})
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def use_item(request):
    if request.user.is_authenticated():
        inventory_pk = request.POST.get("inventory_pk")
        inventory = Inventory.objects.filter(user=request.user, box=False, pending=False, pk=inventory_pk).first()
        if inventory != None and inventory.item.usable:
            pet = Pet.objects.filter(user=request.user).first()
            if pet:
                potion_category = Category.objects.filter(name="potion").first()
                if inventory.item.category != potion_category:
                    if inventory.item.hunger != 10: # 50% chance of working
                        if (pet.hunger + inventory.item.hunger) <= 0:
                            pet.hunger = 1
                        elif (pet.hunger + inventory.item.hunger) <= 5:
                            pet.hunger += inventory.item.hunger
                        else:
                            pet.hunger = 5
                    else:
                        chance = random.randint(1, 2)
                        if chance == 1:
                            if (pet.hunger + 1) <= 0:
                                pet.hunger = 1
                            elif (pet.hunger + 1) <= 5:
                                pet.hunger += 1
                            else:
                                pet.hunger = 5

                    if inventory.item.wellness != 10: # 50% chance of working
                        if (pet.wellness + inventory.item.wellness) <= 0:
                            pet.wellness = 1
                        elif (pet.wellness + inventory.item.wellness) <= 5:
                            pet.wellness += inventory.item.wellness
                        else:
                            pet.wellness = 5
                    else:
                        chance = random.randint(1, 2)
                        if chance == 1:
                            if (pet.wellness + 1) <= 0:
                                pet.wellness = 1
                            elif (pet.wellness + 1) <= 5:
                                pet.wellness += 1
                            else:
                                pet.wellness = 5

                    if inventory.item.happiness != 10: # 50% chance of working
                        if (pet.happiness + inventory.item.happiness) <= 0:
                            pet.happiness = 1
                        elif (pet.happiness + inventory.item.happiness) <= 5:
                            pet.happiness += inventory.item.happiness
                        else:
                            pet.happiness = 5
                    else:
                        chance = random.randint(1, 2)
                        if chance == 1:
                            if (pet.happiness + 1) <= 0:
                                pet.happiness = 1
                            elif (pet.happiness + 1) <= 5:
                                pet.happiness += 1
                            else:
                                pet.happiness = 5

                    pet.save()

                    # AVATARS
                    sweet_avatar = Avatar.objects.get(url="sweet")
                    if sweet_avatar not in request.user.profile.avatars.all():
                        if pet.color == "sprinkle":
                            if "cupcake" in inventory.item.name.lower():
                                request.user.profile.avatars.add(sweet_avatar)
                                request.user.profile.save()
                                message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Sweet~\" to use on the boards!")

                    inventory.delete()
                    request.session['results'] = "You have used your " + inventory.item.name + "!"
                    return redirect(inventory_page)

                else: # item is a potion
                    color_potion_category = Category.objects.filter(name="color potion").first()
                    morph_potion_category = Category.objects.filter(name="morph potion").first()
                    colormorph_potion_category = Category.objects.filter(name="colormorph potion").first()
                    mystery_potion_category = Category.objects.filter(name="mystery potion").first()
                    stat_potion_category = Category.objects.filter(name="stat potion").first()
                    if inventory.item.second_category == color_potion_category:
                        old_color = pet.color
                        new_color = inventory.item.url.replace("-potion", "")
                        pet.color = new_color
                        pet.all_colors += new_color + " " + pet.animal.name + ","
                        pet.save()
                        inventory.delete()
                        request.session['results'] = "Your " + old_color + " " + pet.animal.name + " has transformed into a " + new_color + " " + pet.animal.name + "!"
                        
                        # AVATARS
                        starry_night_avatar = Avatar.objects.get(url="starry-night")
                        if starry_night_avatar not in request.user.profile.avatars.all():
                            if pet.color == "starry":
                                today = datetime.today()
                                if today.hour > 18 and today.hour < 24 or today.hour > 0 and today.hour < 6:
                                    request.user.profile.avatars.add(starry_night_avatar)
                                    request.user.profile.save()
                                    message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Starry Night\" to use on the boards!")

                        return redirect(potion_results_page)
                    elif inventory.item.second_category == morph_potion_category:
                        old_species = pet.animal.name
                        new_species = Animal.objects.filter(name=inventory.item.url.replace("-potion", "")).first()
                        pet.animal = new_species
                        pet.all_colors += pet.color + " " + new_species.name + ","
                        pet.save()
                        inventory.delete()
                        request.session['results'] = "Your " + old_species + " has transformed into a " + new_species.name + "!"
                        
                        # AVATARS
                        rand_num = random.randint(1, 4)
                        if rand_num == 1:
                            witch_avatar = Avatar.objects.get(url="witch")
                            if witch_avatar not in request.user.profile.avatars.all():
                                request.user.profile.avatars.add(witch_avatar)
                                request.user.profile.save()
                                message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Witch!!!\" to use on the boards!")

                        return redirect(potion_results_page)
                    elif inventory.item.second_category == colormorph_potion_category:
                        old_species = pet.animal.name
                        old_color = pet.color

                        new = inventory.item.url.split("-") # returns color, animal, potion
                        if "knit" in new:
                            new = [
                                    "%s-knit"%(new[0]),
                                    new[2],
                                    new[3]
                                ]
                        new.pop() # remove -potion
                        new_species = Animal.objects.get(name=new[1])
                        new_color = new[0]

                        pet.animal = new_species
                        pet.color = new_color
                        add_color = new_color + " " + new_species.name + ","
                        pet.all_colors += add_color
                        pet.save()
                        inventory.delete()

                        request.session['results'] = "Your " + old_color + " " + old_species + " has transformed into a " + new_color + " " + new_species.name + "!"
                        return redirect(potion_results_page)

                    elif inventory.item.second_category == stat_potion_category:
                        if inventory.item.url.replace("-potion", "") == "hunger":
                            pet.hunger = 5
                            pet.save()
                            inventory.delete()
                            request.session['results'] = "Your pet's hunger is now at maximum!"

                            rand_num = random.randint(1, 4)
                            if rand_num == 1:
                                funny_avatar = Avatar.objects.get(url="that-tasted-funny")
                                if funny_avatar not in request.user.profile.avatars.all():
                                    request.user.profile.avatars.add(funny_avatar)
                                    request.user.profile.save()
                                    message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"That Tasted Funny...\" to use on the boards!")

                            return redirect(potion_results_page)

                        elif inventory.item.url.replace("-potion", "") == "happiness":
                            pet.happiness = 5
                            pet.save()
                            inventory.delete()
                            request.session['results'] = "Your pet's happiness is now at maximum!"
                            return redirect(potion_results_page)

                        elif inventory.item.url.replace("-potion", "") == "wellness":
                            pet.wellness = 5
                            pet.save()
                            inventory.delete()
                            request.session['results'] = "Your pet's wellness is now at maximum!"
                            return redirect(potion_results_page)

                    elif inventory.item.second_category == mystery_potion_category:
                            stat = random.randint(1, 4)
                            change = random.randint(-2, 2)

                            request.session['results'] = "Your pet feels a bit funny..."

                            if stat == 1:
                                pet.hunger += change
                                if pet.hunger <= 1:
                                    pet.hunger == 1
                                elif pet.hunger >= 5:
                                    pet.hunger == 5
                                pet.save()
                                request.session['results'] += " It's hunger changes by a bit."
                            elif stat == 2:
                                pet.wellness += change
                                if pet.wellness <= 1:
                                    pet.wellness == 1
                                elif pet.wellness >= 5:
                                    pet.wellness == 5
                                pet.save()
                                request.session['results'] += " It's wellness changes by a bit."
                            elif stat == 3:
                                pet.happiness += change
                                if pet.happiness <= 1:
                                    pet.happiness == 1
                                elif pet.happiness >= 5:
                                    pet.happiness == 5
                                pet.save()
                                request.session['results'] += " It's happiness changes by a bit."
                            elif stat == 4:
                                change_1 = random.randint(-1, 1)
                                change_2 = random.randint(-1, 1)
                                change_3 = random.randint(-1, 1)
                                pet.hunger += change_1
                                if pet.hunger <= 1:
                                    pet.hunger == 1
                                elif pet.hunger >= 5:
                                    pet.hunger == 5
                                pet.wellness += change_2
                                if pet.wellness <= 1:
                                    pet.wellness == 1
                                elif pet.wellness >= 5:
                                    pet.wellness == 5
                                pet.happiness += change_3
                                if pet.happiness <= 1:
                                    pet.happiness == 1
                                elif pet.happiness >= 5:
                                    pet.happiness == 5
                                pet.save()
                                request.session['results'] += " All of it's stats change a bit."
                            inventory.delete()
                            return redirect(potion_results_page)

                    else:
                        request.session['error'] = "Sorry, that potion was not found."
                        return redirect(error_page)
            else:
                request.session['error'] = "You must have a pet to use an item."
                return redirect(error_page)
        else:
            request.session['error'] = "You cannot use that item at this time."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def potion_results_page(request):
    results = request.session.pop('results', False)
    if results == False:
        results = "We are not sure what went wrong, but we will work on fixing it."
    pet = Pet.objects.filter(user=request.user).first()
    if pet is None:
        request.session['error'] = "You must have a pet to view this page."
        return redirect(error_page)
    return render(request, 'shop/potion_results_page.html', {'results':results, 'pet':pet})

def shop_page(request, shop_url):

    shop = Shop.objects.get(url=shop_url)
    shop_items = Stock.objects.filter(shop=shop)

    # QUEST
    if shop.name == "Alchemist":
        inventory = {"amethyst":Inventory.objects.filter(user=request.user, item__url="big-amethyst-crystal-piece", box=False, pending=False).count(),"aquamarine":Inventory.objects.filter(user=request.user, item__url="big-aquamarine-crystal-piece", box=False, pending=False).count(),"diamond":Inventory.objects.filter(user=request.user, item__url="big-diamond-crystal-piece", box=False, pending=False).count(),"emerald":Inventory.objects.filter(user=request.user, item__url="big-emerald-crystal-piece", box=False, pending=False).count(),"ruby":Inventory.objects.filter(user=request.user, item__url="big-ruby-crystal-piece", box=False, pending=False).count(),"sapphire":Inventory.objects.filter(user=request.user, item__url="big-sapphire-crystal-piece", box=False, pending=False).count(),"topaz":Inventory.objects.filter(user=request.user, item__url="big-topaz-crystal-piece", box=False, pending=False).count()}
        mystery_card = Item.objects.get(url="mystery-card")
        mystery_card = Inventory.objects.filter(user=request.user, item=mystery_card).first()
        bank_card = Item.objects.get(url="deactivated-bank-card")
        bank_card = Inventory.objects.filter(user=request.user, item=bank_card).first()
    else:
        inventory = None
        mystery_card = None
        bank_card = None

    return render(request, 'shop/shop_page.html', {'shop':shop, 'shop_items':shop_items, 'mystery_card':mystery_card, 'inventory':inventory, 'bank_card':bank_card})

def purchase_item(request, shop_url):
    require_login(request)

    item_pk = request.POST.get("item")

    shop = Shop.objects.get(url=shop_url)
    item = Stock.objects.get(pk=item_pk, shop=shop)

    points = request.user.profile.points
    num_items_in_inventory = Inventory.objects.filter(user=request.user, box=False, pending=False).count()

    if not item:
        return handle_error(request, "Sorry, that item is not available at this time.")

    elif num_items_in_inventory >= 50:
        return handle_error(request, "You can only have up to 50 items in your inventory.")

    elif item.price >= points:
        return handle_error(request, "You do not have enough points to buy that item.")

    else:
        request.user.profile.subtract_points(item.price)
        inventory = Inventory.objects.create(user=request.user, item=item.item)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

    # AVATARS

    pet = Pet.objects.filter(user=request.user).first()
    if pet is not None:
        pink_avatar = Avatar.objects.get(url="yay-pink")
        if pink_avatar not in request.user.profile.avatars.all():
            if "pink" in inventory.item.name.lower():
                request.user.profile.avatars.add(pink_avatar)
                request.user.profile.save()
                message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Yay! Pink!!\" to use on the boards!")

    return redirect(shop_page, shop_url)
        

def compound_interest(principal, rate, times_per_year, years):
    # (1 + r/n)
    body = 1 + (rate / times_per_year)
    # nt
    exponent = times_per_year * years
    # P(1 + r/n)^nt
    return principal * pow(body, exponent)

def bank_page(request):
    if request.user.is_authenticated():
        today = datetime.today()
        bank_account = BankAccount.objects.filter(user=request.user).first()
        interest = DailyClaim.objects.filter(user=request.user, daily_type="interest", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
        
        if bank_account != None:
            if bank_account.level == 1:
                rate = 0.1
            elif bank_account.level == 2:
                rate = 0.13
            elif bank_account.level == 3:
                rate = 0.15
            elif bank_account.level == 4:
                rate = 0.16
            else:
                rate = 0.17
            interest_amount = compound_interest(bank_account.balance, rate, 365, 1)
            interest_amount = int((interest_amount - bank_account.balance) / 365)
        else:
            interest_amount = 0
        return render(request, 'shop/bank_page.html', {'bank_account':bank_account, 'interest':interest, 'interest_amount':interest_amount})
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def open_bank_account_page(request):
    if request.user.is_authenticated():
        check_for_bank_account = BankAccount.objects.filter(user=request.user).count()
        if check_for_bank_account == 0:
            error = request.session.pop('error', False)
            return render(request, 'shop/open_bank_account_page.html', {'error':error})
        else:
            request.session['error'] = "Your account has already been opened."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def open_bank_account(request):
    if request.user.is_authenticated():
        check_for_bank_account = BankAccount.objects.filter(user=request.user).count()
        if check_for_bank_account == 0:
            level = int(request.POST.get("level"))

            deposit = request.POST.get("deposit")
            if deposit:
                try:
                    deposit = int(deposit)
                except:
                    request.session['error'] = "Your deposit must be an integer."
                    return redirect(open_bank_account_page)
                if deposit >= 100:
                    if level == 2 and deposit < 10000:
                        request.session['error'] = "To be a Bronze account, your deposit must be at least 10,000 points."
                        return redirect(open_bank_account_page)
                    elif level == 3 and deposit < 100000:
                        request.session['error'] = "To be a Silver account, your deposit must be at least 100,000 points."
                        return redirect(open_bank_account_page)
                    elif level == 4 and deposit < 1000000:
                        request.session['error'] = "To be a Gold account, your deposit must be at least 1,000,000 points."
                        return redirect(open_bank_account_page)
                    elif level == 5 and deposit < 10000000:
                        request.session['error'] = "To be a Platinum account, your deposit must be at least 10,000,000 points."
                        return redirect(open_bank_account_page)

                    if request.user.profile.points >= deposit:
                        bank = BankAccount.objects.create(user=request.user, balance=deposit, level=level)
                        request.user.profile.points -= deposit
                        request.user.profile.save()
                        return redirect(bank_page)
                    else:
                        request.session['error'] = "You must have enough points to cover your deposit."
                        return redirect(open_bank_account_page)
                else:
                    request.session['error'] = "Your deposit must be at least 100 points."
                    return redirect(open_bank_account_page)
            else:
                request.session['error'] = "Please enter a deposit amount."
                return redirect(open_bank_account_page)
        else:
            request.session['error'] = "Your account has already been opened."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def deposit(request):
    if request.user.is_authenticated():
        bank_account = BankAccount.objects.filter(user=request.user).first()
        if bank_account:
            deposit = request.POST.get("amount")
            if deposit:
                try:
                    deposit = int(deposit)
                except:
                    request.session['error'] = "Your deposit must be an integer."
                    return redirect(error_page)
                if request.user.profile.points >= deposit:
                    request.user.profile.points -= deposit
                    request.user.profile.save()
                    bank_account.balance += deposit
                    bank_account.save()

                    # AVATARS
                    riches_avatar = Avatar.objects.get(url="riches")
                    if riches_avatar not in request.user.profile.avatars.all():
                        if bank_account.balance >= 1000000:
                            request.user.profile.avatars.add(riches_avatar)
                            request.user.profile.save()
                            message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Riches!\" to use on the boards!")
                    return redirect(bank_page)
                else:
                    request.session['error'] = "You do not have enough points to make that deposit."
                    return redirect(error_page)
            else:
                request.session['error'] = "Please enter a deposit amount."
                return redirect(error_page)
        else:
            request.session['error'] = "You may not deposit if you do not have a bank account."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)


def withdraw(request):
    if request.user.is_authenticated():
        bank_account = BankAccount.objects.filter(user=request.user).first()
        if bank_account:
            withdraw = request.POST.get("amount")
            if withdraw:
                try:
                    withdraw = int(withdraw)
                except:
                    request.session['error'] = "Your withdraw amount must be an integer."
                    return redirect(error_page)
                if bank_account.balance >= withdraw:
                    request.user.profile.points += withdraw
                    request.user.profile.save()
                    bank_account.balance -= withdraw
                    bank_account.save()
                    return redirect(bank_page)
                else:
                    request.session['error'] = "You do not have enough points in your bank to make that withdraw."
                    return redirect(error_page)
            else:
                request.session['error'] = "Please enter a withdraw amount."
                return redirect(error_page)
        else:
            request.session['error'] = "You may not withdraw if you do not have a bank account."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def collect_interest(request):
    if request.user.is_authenticated():
        bank_account = BankAccount.objects.filter(user=request.user).first()
        if bank_account:
            today = datetime.today()
            #interest = Interest.objects.filter(user=request.user).first()
            if bank_account.level == 1:
                rate = 0.1
            elif bank_account.level == 2:
                rate = 0.13
            elif bank_account.level == 3:
                rate = 0.15
            elif bank_account.level == 4:
                rate = 0.16
            else:
                rate = 0.17
            interest_amount = compound_interest(bank_account.balance, rate, 365, 1)
            interest_amount = int((interest_amount - bank_account.balance) / 365)
            interest = DailyClaim.objects.filter(user=request.user, daily_type="interest", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
            if not interest:
                bank_account.balance += interest_amount
                bank_account.save()
                interest = DailyClaim.objects.create(user=request.user, message="You have already collected your interest today.", daily_type="interest", points=interest_amount)
                return redirect(bank_page)
            else:
                request.session['error'] = "You have already collected your interest today."
                return redirect(error_page)
        else:
            request.session['error'] = "You may not collect interest if you do not have a bank account."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def upgrade_bank_account(request):
    if request.user.is_authenticated():
        bank_account = BankAccount.objects.filter(user=request.user).first()
        if bank_account:
            can_upgrade = False
            if bank_account.level == 1 and bank_account.balance >= 10000:
                can_upgrade = True
            elif bank_account.level == 2 and bank_account.balance >= 100000:
                can_upgrade = True
            elif bank_account.level == 3 and bank_account.balance >= 1000000:
                can_upgrade = True
            elif bank_account.level == 4 and bank_account.balance >= 10000000:
                can_upgrade = True

            if can_upgrade:
                bank_account.level += 1
                bank_account.save()
                return redirect(bank_page)
            else:
                request.session['error'] = "You are not eligible to upgrade your bank account at this time."
                return redirect(error_page)
        else:
            request.session['error'] = "You may not upgrade if you do not have a bank account."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def gallery_page(request):
    if request.user.is_authenticated():
        gallery = Gallery.objects.filter(user=request.user).first()
        if gallery:
            plush_category = Category.objects.get(name="plush")
            card_category = Category.objects.get(name="playing card")

            total_available_plush = Item.objects.filter(category=plush_category).count()
            total_available_cards = Item.objects.filter(category=card_category).count()
            inventory_plush = Inventory.objects.filter(user=request.user, item__category=plush_category, box=False, pending=False)
            inventory_cards = Inventory.objects.filter(user=request.user, item__category=card_category, box=False, pending=False)
            gallery_plush = gallery.plush.all().order_by('name')
            gallery_cards = gallery.cards.all().order_by('name')
            total_items_in_gallery = gallery_plush.count() + gallery_cards.count()

            return render(request, 'shop/gallery_page.html', {'gallery':gallery, 'total_plush':total_available_plush, 'total_cards':total_available_cards, 'user_plush':inventory_plush, 'user_cards':inventory_cards, 'gallery_plush':gallery_plush, 'gallery_cards':gallery_cards, 'total_items_in_gallery':total_items_in_gallery})
        else:
            return render(request, 'shop/gallery_page.html', {'gallery':gallery})
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def user_gallery_page(request, username):
    user = User.objects.filter(username=username).first()
    if user:
        gallery = Gallery.objects.filter(user=user).first()
        if gallery:
            plush_category = Category.objects.get(name="plush")
            card_category = Category.objects.get(name="playing card")
            total_available_plush = Item.objects.filter(category=plush_category).count()
            total_available_cards = Item.objects.filter(category=card_category).count()
            gallery_plush = gallery.plush.all().order_by('name')
            gallery_cards = gallery.cards.all().order_by('name')
            return render(request, 'shop/user_gallery_page.html', {'gallery':gallery, 'total_plush':total_available_plush, 'gallery_plush':gallery_plush, 'total_cards':total_available_cards, 'gallery_cards':gallery_cards})
        else:
            request.session['error'] = "That user does not yet have a gallery."
            return redirect(error_page)
    else:
        request.session['error'] = "No user with that username exists."
        return redirect(error_page)


def open_gallery_page(request):
    if request.user.is_authenticated():
        gallery = Gallery.objects.filter(user=request.user).first()
        if gallery is None:
            return render(request, 'shop/open_gallery_page.html')
        else:
            request.session['error'] = "You have already created a gallery."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def open_gallery(request):
    if request.user.is_authenticated():
        gallery = Gallery.objects.filter(user=request.user).first()
        if gallery is None:
            if request.user.profile.points >= 500:
                request.user.profile.points -= 500
                request.user.profile.save()
                gallery = Gallery.objects.create(user=request.user, name=request.POST.get("gallery_name"))
                return redirect(gallery_page)
            else:
                request.session['error'] = "You do not have enough points to open a gallery."
                return redirect(error_page)
        else:
            request.session['error'] = "You have already created a gallery."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def add_gallery_item(request):
    if request.user.is_authenticated():
        gallery = Gallery.objects.filter(user=request.user).first()
        if gallery:
            item = request.POST.get("item")
            try:
                item = int(item)
            except:
                request.session['error'] = "That item does not exist."
                return redirect(error_page)

            item = Inventory.objects.filter(user=request.user, pk=item, box=False, pending=False).first()
            if item:
                if (gallery.plush.count() + gallery.cards.count()) < gallery.space:
                    if item.item.category.name == "plush":
                        if item.item not in gallery.plush.all():
                            if gallery.plush.count() == 9: # will now become 10
                                subject = "Congratulations!"
                                text = "You have just reached 10 plushies in your gallery! You have been awarded the Amateur Plushie Collector Badge."
                                message = Message.objects.create(receiving_user=request.user, subject=subject, text=text)
                                badge = Badge.objects.create(user=request.user, rank="amateur", area="plush-collecting")
                            elif gallery.plush.count() == 49: # will now become 50
                                subject = "Congratulations!"
                                text = "You have just reached 10 plushies in your gallery! You have been awarded the Professional Plushie Collector Badge."
                                message = Message.objects.create(receiving_user=request.user, subject=subject, text=text)
                                badge = Badge.objects.create(user=request.user, rank="professional", area="plush-collecting")

                            gallery.plush.add(item.item)
                            gallery.save()
                            item.delete()

                            # AVATARS
                            historic_avatar = Avatar.objects.get(url="historic")
                            if historic_avatar not in request.user.profile.avatars.all():
                                pet = Pet.objects.filter(user=request.user).first()
                                if pet is not None:
                                    if pet.color == "baroque":
                                        request.user.profile.avatars.add(historic_avatar)
                                        request.user.profile.save()
                                        message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Historic\" to use on the boards!")

                            return redirect(gallery_page)
                        else:
                            request.session['error'] = "That item is already in your gallery."
                            return redirect(error_page)
                    elif item.item.category.name == "playing card":
                        if item.item not in gallery.cards.all():
                            if gallery.cards.count() == 9: # will now become 10
                                subject = "Congratulations!"
                                text = "You have just reached 10 cards in your gallery! You have been awarded the Amateur Card Collector Badge."
                                message = Message.objects.create(receiving_user=request.user, subject=subject, text=text)
                                badge = Badge.objects.create(user=request.user, rank="amateur", area="card-collecting")
                            elif gallery.cards.count() == 49: # will now become 50
                                subject = "Congratulations!"
                                text = "You have just reached 10 cards in your gallery! You have been awarded the Professional Card Collector Badge."
                                message = Message.objects.create(receiving_user=request.user, subject=subject, text=text)
                                badge = Badge.objects.create(user=request.user, rank="professional", area="card-collecting")

                            gallery.cards.add(item.item)
                            gallery.save()
                            item.delete()

                            # AVATARS
                            pet = Pet.objects.filter(user=request.user).first()
                            if pet is not None:
                                if pet.color == "baroque":
                                    historic_avatar = Avatar.objects.get(url="historic")
                                    request.user.profile.avatars.add(historic_avatar)
                                    request.user.profile.save()
                                    message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Historic\" to use on the boards!")

                            return redirect(gallery_page)
                        else:
                            request.session['error'] = "That item is already in your gallery."
                            return redirect(error_page)
                else:
                    request.session['error'] = "Your gallery is full right now."
                    return redirect(error_page)
            else:
                request.session['error'] = "That item does not exist."
                return redirect(error_page)
        else:
            request.session['error'] = "You have not yet created a gallery."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)


def upgrade_gallery(request):
    if request.user.is_authenticated():
        gallery = Gallery.objects.filter(user=request.user).first()
        if gallery:
            if request.user.profile.points >= gallery.upgrade_cost:
                request.user.profile.points -= gallery.upgrade_cost
                request.user.profile.save()

                gallery.space += 5
                gallery.upgrade_cost = 100*gallery.space
                gallery.save()
                return redirect(gallery_page)
            else:
                request.session['error'] = "You do not have enough points to upgrade your gallery."
                return redirect(error_page)
        else:
            request.session['error'] = "You have not yet created a gallery."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def rename_gallery(request):
    if request.user.is_authenticated():
        gallery = Gallery.objects.filter(user=request.user).first()
        if gallery:
            new_gallery_name = request.POST.get("new_gallery_name")
            gallery.name = new_gallery_name
            gallery.save()
            return redirect(gallery_page)
        else:
            request.session['error'] = "You have not yet created a gallery."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def your_shop_page(request):
    if request.user.is_authenticated():
        shop = UserShop.objects.filter(user=request.user).first()
        user_items = Inventory.objects.filter(user=request.user, box=False, pending=False)
        if shop:
            if shop.items is not None and shop.items != ",":
                shop_items = shop.items.split(",")
                shop_items.pop()
                for n in range(0, len(shop_items)):
                    shop_items[n] = shop_items[n].split(".")
                    shop_items[n][0] = Item.objects.filter(url=shop_items[n][0]).first()
                    shop_items[n][1] = int(shop_items[n][1])
                    n += 1
            else:
                shop_items = None
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

            item = Inventory.objects.filter(user=request.user, pk=item, box=False, pending=False).first()
            if item:
                if shop.items is not None:
                    shop_items = shop.items.split(",")
                    shop_items.pop()
                    item_count = len(shop_items)
                else:
                    item_count = 0
                if item_count < shop.space:
                    price = request.POST.get("price")
                    try:
                        price = int(price)
                    except:
                        request.session['error'] = "Price must be an integer."
                        return redirect(error_page)

                    if shop.items is not None:
                        shop.items += item.item.url + "." + str(price) + ","
                    else:
                        shop.items = item.item.url + "." + str(price) + ","
                    item.delete()
                    shop.save()
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
                item_pk = request.POST.get("item")
                item = Item.objects.filter(pk=item_pk).first()
                if item:
                    shop_items = shop.items.split(",")
                    shop_items.pop()
                    for n in range(0, len(shop_items)):
                        shop_items[n] = shop_items[n].split(".")
                        shop_items[n][0] = Item.objects.filter(url=shop_items[n][0]).first()
                        shop_items[n][1] = int(shop_items[n][1])
                        if shop_items[n][0] == item:
                            shop_items[n][1] = price
                        n += 1

                    for n in range(0, len(shop_items)):
                        shop_items[n][0] = shop_items[n][0].url
                        shop_items[n][1] = str(shop_items[n][1])
                        shop_items[n] = ".".join(shop_items[n])

                    shop.items = ",".join(shop_items)
                    shop.items += ","
                    shop.save()
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
                item_pk = request.POST.get("item")
                item = Item.objects.filter(pk=item_pk).first()
                index = int(request.POST.get("index"))
                if item:
                    shop_items = shop.items.split(",")
                    shop_items.pop()

                    n = 0
                    while (n<len(shop_items)):
                        shop_items[n] = shop_items[n].split(".")
                        shop_items[n][0] = Item.objects.filter(url=shop_items[n][0]).first()
                        if shop_items[n][0] == item:
                            if n == index:
                                all_inventory = Inventory.objects.filter(user=request.user, box=False, pending=False).count()
                                if all_inventory < 50:
                                    inventory = Inventory.objects.create(user=request.user, item=item)
                                else:
                                    request.session['error'] = "You can only have up to 50 items in your inventory."
                                    return redirect(error_page)
                                shop_items.pop(n)
                                n -= 1
                                index = None
                        n += 1

                    for n in range(0, len(shop_items)):
                        shop_items[n][0] = shop_items[n][0].url
                        shop_items[n][1] = str(shop_items[n][1])
                        shop_items[n] = ".".join(shop_items[n])

                    shop.items = ",".join(shop_items)
                    shop.items += ","
                    shop.save()

                    if shop.items == ",":
                        shop.items = None
                        shop.save()
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
            if shop.items is not None and shop.items != ",":
                shop_items = shop.items.split(",")
                shop_items.pop()
                for n in range(0, len(shop_items)):
                    shop_items[n] = shop_items[n].split(".")
                    shop_items[n][0] = Item.objects.filter(url=shop_items[n][0]).first()
                    shop_items[n][1] = int(shop_items[n][1])
                    n += 1
            else:
                shop_items = None
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
                item_pk = request.POST.get("item_pk")
                item = Item.objects.filter(pk=item_pk).first()
                index = int(request.POST.get("index"))
                if item:
                    shop_items = shop.items.split(",")
                    shop_items.pop()

                    n = 0
                    while (n<len(shop_items)):
                        shop_items[n] = shop_items[n].split(".")
                        shop_items[n][0] = Item.objects.filter(url=shop_items[n][0]).first()
                        if shop_items[n][0] == item:
                            if n == index:
                                all_inventory = Inventory.objects.filter(user=request.user, box=False, pending=False).count()
                                if all_inventory < 50:
                                    inventory = Inventory.objects.create(user=request.user, item=item)
                                else:
                                    request.session['error'] = "You can only have up to 50 items in your inventory."
                                    return redirect(error_page)
                                if request.user.profile.points >= int(shop_items[n][1]):
                                    request.user.profile.points -= int(shop_items[n][1])
                                    request.user.profile.save()
                                else:
                                    request.session['error'] = "You do not have enough points to buy that item."
                                    return redirect(error_page)
                                shop_items.pop(n)
                                n -= 1
                                index = None
                        n += 1

                    for n in range(0, len(shop_items)):
                        shop_items[n][0] = shop_items[n][0].url
                        shop_items[n][1] = str(shop_items[n][1])
                        shop_items[n] = ".".join(shop_items[n])

                    shop.items = ",".join(shop_items)
                    shop.items += ","
                    shop.save()

                    if shop.items == ",":
                        shop.items = None
                        shop.save()
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

def shop_search_results_page(request):
    user_shops = UserShop.objects.all()
    keyword = request.POST.get("keyword")
    if keyword is not None and keyword != "":
        original_keyword = keyword
        keyword = keyword.replace(" ", "-")
        keyword = keyword.lower()
        shops_with_keyword = []
        for shop in user_shops:
            if keyword.lower() in shop.items:
                shop_items = shop.items.split(",")
                shop_items.pop()
                for item in shop_items:
                    if keyword in item:
                        new_item = [shop, "", ""]
                        item = item.split(".")
                        returned_item = Item.objects.filter(url=item[0]).first()
                        new_item[1] = returned_item
                        new_item[2] = int(item[1])
                        shops_with_keyword.append(new_item)

        # take random ones from list and order those, as to not always show lowest prices
        random.shuffle(shops_with_keyword)
        shops_with_keyword = shops_with_keyword[:10]

        shops_with_keyword = sorted(shops_with_keyword, key=itemgetter(2))
        shops_with_keyword = tuple(shops_with_keyword)

        keyword = original_keyword
        
        return render(request, 'shop/shop_search_results_page.html', {'keyword':keyword, 'shops_with_keyword':shops_with_keyword})
    else:
        request.session['error'] = "You must type a keyword to search."
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

def safety_deposit_box_page(request):
    if request.user.is_authenticated():
        inventory_items = Inventory.objects.filter(user=request.user, box=False, pending=False)
        box_items = Inventory.objects.filter(user=request.user, box=True)
        return render(request, 'shop/safety_deposit_box_page.html', {'box_items':box_items, 'inventory_items':inventory_items})
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def add_box_item(request):
    if request.user.is_authenticated():
        item = request.POST.get("item")
        item = Inventory.objects.filter(user=request.user, box=False, pending=False, pk=item).first()
        if item:
            box_items = Inventory.objects.filter(user=request.user, box=True).count()
            if box_items < request.user.profile.box_size:
                item.box = True
                item.save()
                return redirect(safety_deposit_box_page)
            else:
                request.session['error'] = "Your Safety Deposit Box is already full. Please remove something or upgrade to add more."
                return redirect(error_page)
        else:
            request.session['error'] = "No item with that index exists."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def remove_box_item(request, item):
    if request.user.is_authenticated():
        item = Inventory.objects.filter(user=request.user, pk=item).first()
        if item:
            inventory_items = Inventory.objects.filter(user=request.user, box=False, pending=False).count()
            if inventory_items < 50:
                item.box = False
                item.save()
                return redirect(safety_deposit_box_page)
            else:
                request.session['error'] = "You can only have up to 50 items in your inventory."
                return redirect(error_page)
        else:
            request.session['error'] = "No item with that index exists."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def upgrade_box(request):
    if request.user.is_authenticated():
        if request.user.profile.points >= 1000:
            request.user.profile.subtract_points(1000)
            request.user.profile.box_size += 5
            request.user.profile.save()
            return redirect(safety_deposit_box_page)
        else:
            request.session['error'] = "You do not have enough points to upgrade your Safety Deposit Box."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def trading_post_page(request):
    if request.user.is_authenticated():
        all_open_trades = Trade.objects.filter(original_trade=None).order_by('-date')
        paginator = Paginator(all_open_trades, 10)
        page = request.GET.get("page")
        if page:
            try:
                page = int(page)
            except:
                request.session['error'] = "Page must be an integer."
                return redirect(error_page)
            all_trades = paginator.page(page)
        else:
            all_trades = paginator.page(1)

        return render(request, 'shop/trading_post_page.html', {'all_trades':all_trades})
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def open_trade_page(request):
    if request.user.is_authenticated():
        inventory = Inventory.objects.filter(user=request.user, box=False, pending=False)
        return render(request, 'shop/open_trade_page.html', {'inventory':inventory})
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def open_trade(request):
    if request.user.is_authenticated():
        items = request.POST.get("items")
        message = request.POST.get("message")
        if items:
            items = items.split(",")
            items_to_trade = []
            for item in items:
                item = int(item)
                item = Inventory.objects.filter(user=request.user, box=False, pending=False, pk=item).first()
                if item is None:
                    request.session['error'] = "All items must be your own."
                    return redirect(error_page)    
                items_to_trade.append(item)
            if len(items_to_trade) <= 5:

                trade = Trade.objects.create(sending_user=request.user, message=message)
                trade.save()
                for item in items_to_trade:
                    item.pending = True
                    item.save()
                    trade.items.add(item)
                    trade.save()

                return redirect(trading_post_page)
            else:
                request.session['error'] = "You may only trade up to five items at a time."
                return redirect(error_page) 
        else:
            request.session['error'] = "You must select at least one item."
            return redirect(error_page)    
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def your_trades_page(request):
    if request.user.is_authenticated():
        your_trades = Trade.objects.filter(sending_user=request.user, original_trade=None).order_by('-date')
        your_offers = Trade.objects.filter(sending_user=request.user).exclude(original_trade=None).order_by('-date')
        
        for trade in your_trades:
            trade.offers = Trade.objects.filter(original_trade=trade).order_by('-date')
        return render(request, 'shop/your_trades_page.html', {'your_trades':your_trades, 'your_offers':your_offers})
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def make_offer_page(request, pk):
    if request.user.is_authenticated():
        original = Trade.objects.filter(pk=pk).first()
        if original:
            inventory = Inventory.objects.filter(user=request.user, box=False, pending=False)
            return render(request, 'shop/make_offer_page.html', {'original':original, 'inventory':inventory})
        else:
            request.session['error'] = "That trade was not found."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def make_offer(request):
    if request.user.is_authenticated():
        original = int(request.POST.get('original'))
        original = Trade.objects.filter(pk=original).first()
        if original:
            items = request.POST.get("items")
            message = request.POST.get("message")
            if items:
                items = items.split(",")
                items_to_trade = []
                for item in items:
                    item = int(item)
                    item = Inventory.objects.filter(user=request.user, box=False, pending=False, pk=item).first()
                    if item is None:
                        request.session['error'] = "All items must be your own."
                        return redirect(error_page)    
                    items_to_trade.append(item)
                if len(items_to_trade) <= 5:

                    trade = Trade.objects.create(original_trade=original, sending_user=request.user, message=message)
                    trade.save()
                    for item in items_to_trade:
                        item.pending = True
                        item.save()
                        trade.items.add(item)
                        trade.save()

                    message = Message.objects.create(receiving_user=original.sending_user, subject="You have received an offer on your trade!", text=request.user.username + " has sent an offer on your trade. Check your trades and offers page to see it.")
                    return redirect(your_trades_page)

                else:
                    request.session['error'] = "You may only trade up to five items at a time."
                    return redirect(error_page)
            else:
                request.session['error'] = "You must select at least one item."
                return redirect(error_page)  
        else:
            request.session['error'] = "That trade was not found."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def accept_offer(request, original_pk, offer_pk):
    if request.user.is_authenticated():
        original_trade = Trade.objects.filter(sending_user=request.user, pk=original_pk).first()
        offer = Trade.objects.filter(pk=offer_pk, original_trade=original_trade).first()
        if original_trade and offer:
            for item in original_trade.items.all():
                item.user = offer.sending_user
                item.pending = False
                item.save()
            for item in offer.items.all():
                item.user = original_trade.sending_user
                item.pending = False
                item.save()
            message = Message.objects.create(receiving_user=original_trade.sending_user, subject="The trade has been completed!", text="The items can be found in your inventory. Note that if you now have over fifty items, you will not be able to get any more unless you remove some first.")
            message = Message.objects.create(receiving_user=offer.sending_user, subject="Your offer has been accepted!", text="The items can be found in your inventory. Note that if you now have over fifty items, you will not be able to get any more unless you remove some first.")

            rejected_offers = Trade.objects.filter(original_trade=original_trade).exclude(pk=offer_pk)
            for offer in rejected_offers:
                message = Message.objects.create(receiving_user=offer.sending_user, subject="Your offer has been rejected.", text="Sorry, but your offer has been rejected. The items have been put back in your inventory. Note that if you now have over fifty items, you will not be able to get any more unless you remove some first.")           
                for item in offer.items.all():
                    item.pending = False
                    item.save()
                offer.delete()

            # AVATARS
            trading_cards_avatar = Avatar.objects.get(url="trading-cards")
            if trading_cards_avatar not in request.user.profile.avatars.all():
                can_get_av = True
                for item in original_trade.items.all():
                    if item.item.category != Category.objects.get(name="playing card"):
                        can_get_av = False
                        break
                for item in offer.items.all():
                    if item.item.category != Category.objects.get(name="playing card"):
                        can_get_av = False
                        break
                if can_get_av:
                    request.user.profile.avatars.add(trading_cards_avatar)
                    request.user.profile.save()
                    message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Trading Cards\" to use on the boards!")

                    if trading_cards_avatar not in offer.sending_user.profile.avatars.all():
                        offer.sending_user.profile.avatars.add(trading_cards_avatar)
                        offer.sending_user.profile.save()
                        message = Message.objects.create(receiving_user=offer.sending_user, subject="You just found a secret avatar!", text="You have just received the avatar \"Trading Cards\" to use on the boards!")
        

            original_trade.delete()
            offer.delete()
            return redirect(your_trades_page)
        else:
            request.session['error'] = "Those trades were not found."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def cancel_trade(request, trade_pk):
    if request.user.is_authenticated():
        trade = Trade.objects.filter(sending_user=request.user, pk=trade_pk, original_trade=None).first()
        if trade:
            message = Message.objects.create(receiving_user=trade.sending_user, subject="Your trade has been cancelled.", text="The items have been put back in your inventory. Note that if you now have over fifty items, you will not be able to get any more unless you remove some first.")  
            for item in trade.items.all():
                item.pending=False
                item.save()

            rejected_offers = Trade.objects.filter(original_trade=trade)
            for offer in rejected_offers:
                message = Message.objects.create(receiving_user=offer.sending_user, subject="Your offer has been rejected.", text="Sorry, but your offer has been rejected. The items have been put back in your inventory. Note that if you now have over fifty items, you will not be able to get any more unless you remove some first.")           
                for item in offer.items.all():
                    item.pending = False
                    item.save()
                offer.delete()
            trade.delete()

            return redirect(your_trades_page)
        else:
            request.session['error'] = "Those trades were not found."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)








