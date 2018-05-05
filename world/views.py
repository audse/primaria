from django.shortcuts import render, redirect

from datetime import datetime
import random

from .models import Score, DailyClaim, MedicinePickup
from shop.models import Shop, Item, Category, Inventory
from social.models import Message, Badge
from core.models import Pet, Avatar
from core.views import error_page, successful_create_pet_page

from shop.views import shop_page
from goddess.views import goddess_commerce_page

def world_page(request):
    # shops = Shop.objects.all().order_by('name')
    city_shops = Shop.objects.filter(location="city").order_by('name')
    suburb_shops = Shop.objects.filter(location="suburbs").order_by('name')
    reservoir_shops = Shop.objects.filter(location="reservoir").order_by('name')
    caves_shops = Shop.objects.filter(location="caves").order_by('name')
    beach_shops = Shop.objects.filter(location="beach").order_by('name')
    return render(request, 'world/world_page.html', {'city_shops':city_shops, 'suburb_shops':suburb_shops, 'reservoir_shops':reservoir_shops, 'caves_shops':caves_shops, 'beach_shops':beach_shops})

def garden_page(request):
    today = datetime.today()
    if request.user.is_authenticated():
        claim = DailyClaim.objects.filter(user=request.user, daily_type="garden", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
    else:
        claim = None
    return render(request, 'world/garden_page.html', {'claim':claim})

def garden_gather(request):
    today = datetime.today()
    if request.user.is_authenticated():
        claims = DailyClaim.objects.filter(user=request.user, daily_type="garden", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).count()
        if claims == 0:
            gathered = request.POST.get("gather")
            if gathered == "inspiration":
                find_something = random.choice([True, True, True, False])
                if find_something:
                    points = random.randint(100,500)
                    message = "You spend some time looking, and notice " + str(points) + " points on the ground. Thankfully no one else was observant enough to see you take them!"
                    claim = DailyClaim.objects.create(user=request.user, daily_type="garden", message=message, points=points)
                    request.user.profile.points += points
                    request.user.profile.save()
                    return redirect(garden_page)
                else:
                    message = "You spend some time looking, and eventually get bored and leave."
                    claim = DailyClaim.objects.create(user=request.user, daily_type="garden", message=message)
                    
                    # AVATARS
                    pet = Pet.objects.filter(user=request.user).first()
                    if pet is not None:
                        aesthetic_avatar = Avatar.objects.get(url="aesthetic")
                        if aesthetic_avatar not in request.user.profile.avatars.all():
                            if pet.color == "opalescent" or pet.color == "marble":
                                request.user.profile.avatars.add(aesthetic_avatar)
                                request.user.profile.save()
                                message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"A E S T H E T I C\" to use on the boards!")
                    
                    return redirect(garden_page)
            elif gathered == "roses":
                find_something = random.choice([True, True, False])
                if find_something:
                    book_category = Category.objects.filter(name="book").first()
                    books = Item.objects.filter(category=book_category)
                    book = random.choice(books)
                    message = "You look around in the bushes, and find a book (" + book.name + ") that was accidentally left here. No one notices when you slip it into your bag..."
                    claim = DailyClaim.objects.create(user=request.user, daily_type="garden", message=message, reward=book)
                    
                    items_in_inventory = Inventory.objects.filter(user=request.user, box=False, pending=False).count()
                    if items_in_inventory < 50:
                        inventory = Inventory.objects.create(user=request.user, item=book)

                        # AVATARS
                        thinker_avatar = Avatar.objects.get(url="thinker")
                        if thinker_avatar not in request.user.profile.avatars.all():
                            if inventory.item.second_category == Category.objects.get("philosophy genre"):
                                request.user.profile.avatars.add(thinker_avatar)
                                request.user.profile.save()
                                message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Thinker\" to use on the boards!")
                    else:
                        message += "But your bag is full! You put it back where you found it."
                    return redirect(garden_page)
                else:
                    message = "Some people seem to notice your attempted thievery, and you get embarrassed and stop."
                    claim = DailyClaim.objects.create(user=request.user, daily_type="garden", message=message)
                    return redirect(garden_page)
        else:
            request.session['error'] = "You have already gathered from the rose garden today."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def hospital_page(request):
    if request.user.is_authenticated():
        pet = Pet.objects.filter(user=request.user).first()
        medicine = MedicinePickup.objects.filter(user=request.user).first()
    else:
        pet = None
        medicine = None
    return render(request, 'world/hospital_page.html', {'pet':pet, 'medicine':medicine})

def make_hospital_appointment(request):
    if request.user.is_authenticated():
        pet = Pet.objects.filter(user=request.user).first()
        if pet:
            if pet.wellness < 3:
                medicine = MedicinePickup.objects.filter(user=request.user).first()
                if medicine is None:
                    if request.user.profile.points >= 500:
                        request.user.profile.points -= 500
                        request.user.profile.save()
                        category = Category.objects.filter(name="medicine").first()
                        medicine = Item.objects.filter(category=category).order_by('?').first()
                        medicine_pickup = MedicinePickup.objects.create(user=request.user, item=medicine)
                        return redirect(hospital_page)
                    else:
                        request.session['error'] = "You do not have enough points to make a hospital appointment."
                        return redirect(error_page)
                else:
                    request.session['error'] = "You cannot make hospital appointment when you already have medicine to pick up."
                    return redirect(error_page)
            else:
                request.session['error'] = "Your pet is not sick enough to make a hospital appointment."
                return redirect(error_page)
        else:
            request.session['error'] = "You must have a pet to view this page."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def pickup_hospital_medicine(request):
    if request.user.is_authenticated():
        pet = Pet.objects.filter(user=request.user).first()
        if pet:
            medicine = MedicinePickup.objects.filter(user=request.user).first()
            if medicine is not None:
                if request.user.profile.points >= 250:
                    if Inventory.objects.filter(user=request.user, box=False, pending=False).count() < 50:
                        request.user.profile.points -= 250
                        request.user.profile.save()
                        inventory = Inventory.objects.create(user=request.user, item=medicine.item)
                        medicine.delete()
                        return redirect(hospital_page)
                    else:
                        request.session['error'] = "You can only have up to 50 items in your inventory."
                        return redirect(error_page)
                else:
                    request.session['error'] = "You do not have enough points to pick up your medicine."
                    return redirect(error_page)
            else:
                request.session['error'] = "You do not have any medicine to pick up."
                return redirect(error_page)
        else:
            request.session['error'] = "You must have a pet to view this page."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def games_page(request):
    return render(request, 'world/games_page.html')

def blackjack_page(request):
    today = datetime.today()
    if request.user.is_authenticated():
        scores_sent = Score.objects.filter(user=request.user, game="blackjack", date__year=today.year, date__month=today.month, date__day=today.day).count()
    else:
        scores_sent = 0
    return render(request, 'world/blackjack_page.html', {'scores_sent':scores_sent})

def tictactoe_page(request):
    today = datetime.today()
    if request.user.is_authenticated():
        scores_sent = Score.objects.filter(user=request.user, game="tictactoe", date__year=today.year, date__month=today.month, date__day=today.day).count()
    else:
        scores_sent = 0
    return render(request, 'world/tictactoe_page.html', {'scores_sent':scores_sent})

def pyramids_page(request):
    today = datetime.today()
    if request.user.is_authenticated():
        scores_sent = Score.objects.filter(user=request.user, game="pyramids", date__year=today.year, date__month=today.month, date__day=today.day).count()
    else:
        scores_sent = 0
    return render(request, 'world/pyramids_page.html', {'scores_sent':scores_sent})

def wheel_serendipity_page(request):
    today = datetime.today()
    if request.user.is_authenticated():
        score = Score.objects.filter(user=request.user, game="serendipity", date__year=today.year, date__month=today.month, date__day=today.day).first()
    else:
        score = None
    return render(request, 'world/wheel_serendipity_page.html', {'score':score})

def wheel_plush_page(request):
    today = datetime.today()
    if request.user.is_authenticated():
        score = Score.objects.filter(user=request.user, game="plush", date__year=today.year, date__month=today.month, date__day=today.day).first()
    else:
        score = None
    return render(request, 'world/wheel_plush_page.html', {'score':score})


def send_score(request, game):
    if request.user.is_authenticated():
        if request.POST.get("score") == "success":
            today = datetime.today()
            scores_sent = Score.objects.filter(user=request.user, game=game, date__year=today.year, date__month=today.month, date__day=today.day).count()
            
            scores_sendable = 0
            points_earned = 0
            if game == "blackjack":
                scores_sendable = 10
                points_earned = 50
            elif game == "tictactoe":
                scores_sendable = 15
                points_earned = 25

            if scores_sent < scores_sendable:
                score = Score.objects.create(user=request.user, game=game)

                request.user.profile.points += points_earned
                request.user.profile.save()

                all_scores = Score.objects.filter(user=request.user).count()
                if all_scores == 100:
                    subject = "Congratulations!"
                    text = "You have just reached 100 total scores sent in games! You have been awarded the Amateur Gamer Badge."
                    message = Message.objects.create(receiving_user=request.user, subject=subject, text=text)
                    badge = Badge.objects.create(user=request.user, rank="amateur", area="gamer")
                elif all_scores == 1000:
                    subject = "Congratulations!"
                    text = "You have just reached 1,000 total scores sent in games! You have been awarded the Professional Gamer Badge."
                    message = Message.objects.create(receiving_user=request.user, subject=subject, text=text)
                    badge = Badge.objects.create(user=request.user, rank="professional", area="gamer")
                elif all_scores == 3000:
                    subject = "Congratulations!"
                    text = "You have just reached 3000 total scores sent in games! You have been awarded the Expert Gamer Badge."
                    message = Message.objects.create(receiving_user=request.user, subject=subject, text=text)
                    badge = Badge.objects.create(user=request.user, rank="expert", area="gamer")

                if game == "blackjack":
                    return redirect(blackjack_page)
                elif game == "tictactoe":
                    return redirect(tictactoe_page)
            else:
                error = "You've already sent the maximum scores for this game today."
                request.session['error'] = error
                return redirect(error_page)
        elif request.POST.get("score") is None:

            # AVATARS
            cheat_avatar = Avatar.objects.get(url="pumpkin-eater")
            if cheat_avatar not in request.user.profile.avatars.all():
                request.user.profile.avatars.add(cheat_avatar)
                request.user.profile.save()
                message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Pumpkin-Eater\" to use on the boards!")

            error = "No cheating, please! That ruins the fun for everyone."
            request.session['error'] = error
            return redirect(error_page)
        elif request.POST.get("score") is not "false":
            score = request.POST.get("score")
            if game != "plush":
                try:
                    score = int(score)
                except:

                    # AVATARS
                    cheat_avatar = Avatar.objects.get(url="pumpkin-eater")
                    if cheat_avatar not in request.user.profile.avatars.all():
                        request.user.profile.avatars.add(cheat_avatar)
                        request.user.profile.save()
                        message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Pumpkin-Eater\" to use on the boards!")

                    error = "No cheating, please! That ruins the fun for everyone."
                    request.session['error'] = error
                    return redirect(error_page)
            else:
                if score == "Plush!":
                    score = 1
                else:
                    score = 0

            if game == "pyramids" and score > 1400: 

                # AVATARS
                cheat_avatar = Avatar.objects.get(url="pumpkin-eater")
                if cheat_avatar not in request.user.profile.avatars.all():
                    request.user.profile.avatars.add(cheat_avatar)
                    request.user.profile.save()
                    message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Pumpkin-Eater\" to use on the boards!")

                error = "No cheating, please! That ruins the fun for everyone."
                request.session['error'] = error
                return redirect(error_page)
            elif game == "serendipity" and score > 3000:

                # AVATARS
                cheat_avatar = Avatar.objects.get(url="pumpkin-eater")
                if cheat_avatar not in request.user.profile.avatars.all():
                    request.user.profile.avatars.add(cheat_avatar)
                    request.user.profile.save()
                    message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Pumpkin-Eater\" to use on the boards!")

                error = "No cheating, please! That ruins the fun for everyone."
                request.session['error'] = error
                return redirect(error_page)
            elif game == "plush" and score not in [0, 1]:
                # AVATARS
                cheat_avatar = Avatar.objects.get(url="pumpkin-eater")
                if cheat_avatar not in request.user.profile.avatars.all():
                    request.user.profile.avatars.add(cheat_avatar)
                    request.user.profile.save()
                    message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Pumpkin-Eater\" to use on the boards!")

                error = "No cheating, please! That ruins the fun for everyone."
                request.session['error'] = error
                return redirect(error_page)    
            else:
                today = datetime.today()
                scores_sent = Score.objects.filter(user=request.user, game=game, date__year=today.year, date__month=today.month, date__day=today.day).count()
                
                scores_sendable = 0
                if game == "pyramids":
                    scores_sendable = 4
                elif game == "serendipity":
                    scores_sendable = 1
                elif game == "plush":
                    scores_sendable = 1

                if scores_sent < scores_sendable: 

                    if game == "plush" and score == 1:
                        item = Item.objects.filter(category__name="plush", rarity=1).order_by('?').first()
                        if Inventory.objects.filter(user=request.user,box=False,pending=False).count() < 50:
                            inventory = Inventory.objects.create(user=request.user, item=item)
                            # score = 0
                            new_score = Score.objects.create(user=request.user, game=game, score=score)
                            return redirect(wheel_plush_page)
                        else:
                            request.session['error'] = "You can only have up to 50 items in your inventory."
                            return redirect(error_page)
                    else:
                        new_score = Score.objects.create(user=request.user, game=game, score=score)

                        request.user.profile.points += score
                        request.user.profile.save()

                        if game == "pyramids":
                            return redirect(pyramids_page)
                        elif game == "serendipity":
                            return redirect(wheel_serendipity_page)
                        elif game == "plush":
                            return redirect(wheel_plush_page)
                else:
                    error = "You've already sent the maximum scores for this game today."
                    request.session['error'] = error
                    return redirect(error_page)
        else:

            # AVATARS
            cheat_avatar = Avatar.objects.get(url="pumpkin-eater")
            if cheat_avatar not in request.user.profile.avatars.all():
                request.user.profile.avatars.add(cheat_avatar)
                request.user.profile.save()
                message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Pumpkin-Eater\" to use on the boards!")

            error = "No cheating, please! That ruins the fun for everyone."
            request.session['error'] = error
            return redirect(error_page)
    else:
        error = "You must be logged in to view this page."
        request.session['error'] = error
        return redirect(error_page)

def pound_page(request):
    pound_pets = Pet.objects.filter(user=None).order_by('?')[:3]
    try:
        pet = Pet.objects.get(user=request.user)
    except:
        pet = None
    return render(request, 'world/pound_page.html', {'pound_pets':pound_pets, 'pet':pet})

def adopt_from_pound(request, adopt):
    if request.user.is_authenticated():
        try:
            pet = Pet.objects.get(user=request.user)
        except:
            pet = None
        if pet == None:
            
            try:
                adopt = Pet.objects.get(name=adopt, user=None)
            except:
                adopt = None

            if adopt != None:
                adopt.user = request.user
                adopt.save()
                return redirect(successful_create_pet_page)
            else:
                request.session['error'] = "No adoptable pet with that name was found."
                return redirect(error_page)
        else:
            request.session['error'] = "You cannot adopt a pet when you already have one."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def give_up_pet(request):
    if request.user.is_authenticated():
        pet = Pet.objects.get(user=request.user).first()
        if pet:
            pet.user = None
            pet.all_colors = pet.color + " " + pet.animal.name
            pet.save()
            return redirect(pound_page)
        else:
            request.session['error'] = "You do not have a pet to give up."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

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
        price = amount * 50
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
                        rarity_set = [None, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2]
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

def dump_page(request):
    success = request.session.pop('success', False)
    dump_items = Inventory.objects.filter(user=None).order_by('?')[:18]
    if request.user.is_authenticated():
        inventory = Inventory.objects.filter(user=request.user, box=False, pending=False)
    else:
        inventory = None
    return render(request, 'world/dump_page.html', {'dump_items':dump_items, 'success':success, 'inventory':inventory})

def take_from_dump(request, pk):
    if request.user.is_authenticated():
        item = Inventory.objects.filter(user=None, pk=pk).first()
        if item:
            item.user = request.user
            item.save()
            request.session['success'] = "You have successfully taken the " + item.item.name + " from the dump!"
            return redirect(dump_page)
        else:
            request.session['error'] = "That item does not exist."
            return redirect(error_page)

    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def dump_item(request):
    if request.user.is_authenticated():
        pk = request.POST.get('item')
        try:
            pk = int(pk)
        except:
            request.session['error'] = "That item does not exist."
            return redirect(error_page)
        item = Inventory.objects.filter(user=request.user, pk=pk).first()
        if item:
            item.user = None
            item.save()
            request.session['success'] = "You have added " + item.item.name + " to the dump..."
            return redirect(dump_page)
        else:
            request.session['error'] = "That item does not exist."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

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
                if request.user.profile.points >= 250:
                    request.user.profile.subtract_points(250)
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

def restricted_area_page(request):
    if request.user.is_authenticated():
        mystery_card = Item.objects.get(url="mystery-card")
        mystery_card = Inventory.objects.filter(user=request.user, item=mystery_card, box=False, pending=False).first()
        activated_card = Item.objects.get(url="activated-area-card")
        activated_card = Inventory.objects.filter(user=request.user, item=activated_card, box=False, pending=False).first()
        
        inventory = Inventory.objects.filter(user=request.user, box=False, pending=False, item__category=Category.objects.get(name="crystal"))
        results = request.session.pop('results', False)
        return render(request, 'world/restricted_area_page.html', {'mystery_card':mystery_card, 'activated_card':activated_card, 'inventory':inventory, 'results':results})
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def update_card(request, crystal):
    if request.user.is_authenticated():
        mystery_card = Item.objects.get(url="mystery-card")
        mystery_card = Inventory.objects.filter(user=request.user, item=mystery_card).first()
        if mystery_card is not None:
            if crystal == "amethyst" or crystal == "aquamarine" or crystal == "diamond" or crystal == "emerald" or crystal == "ruby" or crystal == "sapphire" or crystal == "topaz":
                crystal_item = Item.objects.get(url="big-"+crystal+"-crystal-piece")
                inventory = Inventory.objects.filter(item=crystal_item, user=request.user, box=False, pending=False).first()
                if inventory is not None:
                    inventory.delete()
                    new_card = Item.objects.get(url="deactivated-bank-card")
                    mystery_card.item = new_card
                    mystery_card.save()
                    return redirect(shop_page, "alchemist")
                else:
                    request.session['error'] = "You do not have that crystal to give."
                    return redirect(error_page)
            else:
                request.session['error'] = "That crystal does not exist."
                return redirect(error_page)
        else:     
            request.session['error'] = "You must have a Mystery Card to view this page."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def activate_card(request):
    if request.user.is_authenticated():
        deactivated_card = Item.objects.get(url="deactivated-bank-card")
        deactivated_card = Inventory.objects.filter(item=deactivated_card, user=request.user, box=False, pending=False).first()
        if deactivated_card is not None:
            if request.user.profile.points >= 1000:
                request.user.profile.subtract_points(1000)
                new_card = Item.objects.get(url="activated-area-card")
                deactivated_card.item = new_card
                deactivated_card.save()
                return redirect(goddess_commerce_page)
            else:
                request.session['error'] = "You do not have enough points to activate your card."
                return redirect(error_page)
        else:
            request.session['error'] = "You must have a Deactivated \"Bank Card\" to view this page."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def restricted_machine(request):
    if request.user.is_authenticated():
        activated_card = Item.objects.get(url="activated-area-card")
        activated_card = Inventory.objects.filter(user=request.user, item=activated_card, box=False, pending=False).first()
        if activated_card != None:
            items = request.POST.get("items")
            if items:
                items = items.split(",")
                crystals = []
                for item in items:
                    item = int(item)
                    item = Inventory.objects.filter(item__category=Category.objects.get(name="crystal"), user=request.user, box=False, pending=False, pk=item).first()
                    if item is None:
                        request.session['error'] = "All items must be your own."
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
                    if total_value <= 3: # low chance of rare
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
                    reward = Item.objects.filter(category=potion_category, rarity=rarity).order_by('?').first()
                    inventory = Inventory.objects.create(user=request.user, item=reward)
                    for crystal in crystals:
                        crystal.delete()

                    # AVATARS
                    if random.randint(1, 4) == 1:
                        rulebreaker_avatar = Avatar.objects.get(url="rulebreaker")
                        if rulebreaker_avatar not in request.user.profile.avatars.all():
                            request.user.profile.avatars.add(rulebreaker_avatar)
                            request.user.profile.save()
                            message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Rulebreaker!\" to use on the boards!")
                    
                    request.session['results'] = "You have used your crystals and obtained a new " + reward.name + "!"
                    return redirect(restricted_area_page)

                else:    
                    request.session['error'] = "You cannot use more than three crystals."
                    return redirect(error_page) 
            else:
                request.session['error'] = "You must use at least one crystal."
                return redirect(error_page) 
        else:
            request.session['error'] = "You must have an Activated Area Card to view this page."
            return redirect(error_page) 
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def almighty_meatloaf_page(request):
    if request.user.is_authenticated():
        today = datetime.today()
        loaf_claim = DailyClaim.objects.filter(user=request.user, daily_type="meatloaf", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
    else:
        loaf_claim = None
    return render(request, 'world/almighty_meatloaf_page.html', {'loaf_claim':loaf_claim})

def take_from_meatloaf(request):
    if request.user.is_authenticated():
        today = datetime.today()
        loaf_claim = DailyClaim.objects.filter(user=request.user, daily_type="meatloaf", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
        if loaf_claim is None:
            take_chance = random.randint(1, 8)
            if Inventory.objects.filter(user=request.user, box=False, pending=False).count() < 50:

                # AVATARS
                loaf_avatar = Avatar.objects.get(url="loafing-around")
                if loaf_avatar not in request.user.profile.avatars.all():
                    loaves = Inventory.objects.filter(user=request.user, box=False, pending=False, item__name__icontains="meatloaf").count()
                    if loaves >= 25:
                        request.user.profile.avatars.add(loaf_avatar)
                        request.user.profile.save()
                        message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Loafing Around\" to use on the boards!")
                
                if take_chance != 1:
                    reward = Item.objects.filter(category=Category.objects.get(name="meatloaf")).order_by('?').first()
                    message = "You approach the Almighty and snag a chunk of " + reward.name + " to take home."
                    
                    inventory = Inventory.objects.create(user=request.user, item=reward)
                    claim = DailyClaim.objects.create(user=request.user, daily_type="meatloaf", message=message, reward=reward)
                    return redirect(almighty_meatloaf_page)
                else:
                    message = "You approach the Almighty... but today, it seems you should keep your distance..."
                    claim = DailyClaim.objects.create(user=request.user, daily_type="meatloaf", message=message)
                    return redirect(almighty_meatloaf_page)
            else:
                request.session['error'] = "You can only have up to 50 items in your inventory."
                return redirect(error_page)
        else:
            request.session['error'] = "You have already taken a chunk of meatloaf today."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def trails_page(request):
    if request.user.is_authenticated():
        pet = Pet.objects.filter(user=request.user).first()
        today = datetime.today()
        trails_claim = DailyClaim.objects.filter(user=request.user, daily_type="trails", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
    else:
        pet = None
        trails_claim = None
    return render(request, 'world/trails_page.html', {'pet':pet, 'trails_claim':trails_claim})

def trails(request):
    if request.user.is_authenticated():
        pet = Pet.objects.filter(user=request.user).first()
        if pet:
            today = datetime.today()
            trails_claim = DailyClaim.objects.filter(user=request.user, daily_type="trails", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
            if trails_claim is None:
                stat = random.randint(1, 4)
                if stat == 1: # wellness
                    pet.wellness += random.randint(1, 2)
                    if pet.wellness >= 5:
                        pet.wellness == 5
                    pet.save()

                    message = "You run around the trails with " + pet.name + " and they seem to be feeling healthier already!"
                    claim = DailyClaim.objects.create(user=request.user, daily_type="trails", message=message)

                elif stat == 2: # happiness
                    pet.happiness += random.randint(1, 2)
                    if pet.happiness >= 5:
                        pet.happiness == 5
                    pet.save()

                    message = "You run around the trails with " + pet.name + " and they seem pretty happy!"
                    claim = DailyClaim.objects.create(user=request.user, daily_type="trails", message=message)

                elif stat == 3: # wellness and happiness
                    if pet.happiness < 5:
                        pet.happiness += 1
                    if pet.wellness < 5:
                        pet.wellness += 1
                    pet.save()

                    message = "You run around the trails with " + pet.name + " and they seem completely rejuvinated!"
                    claim = DailyClaim.objects.create(user=request.user, daily_type="trails", message=message)

                else: # nothing
                    message = "You run around the trails with " + pet.name + " but they didn't seem to into it today."
                    claim = DailyClaim.objects.create(user=request.user, daily_type="trails", message=message)

                return redirect(trails_page)
            else:
                request.session['error'] = "Your pet is too tired to run with you on the trails again today."
                return redirect(error_page)
        else:
            request.session['error'] = "You must have a pet to view this page."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def apple_orchard_page(request):
    if request.user.is_authenticated():
        today = datetime.today()
        orchard_claim = DailyClaim.objects.filter(user=request.user, daily_type="orchard", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
    else:
        orchard_claim = None
    return render(request, 'world/daily/apple_orchard_page.html', {'orchard_claim':orchard_claim})

def apple_orchard(request):
    if request.user.is_authenticated():
        today = datetime.today()
        orchard_claim = DailyClaim.objects.filter(user=request.user, daily_type="orchard", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
        if orchard_claim == None:
            if Inventory.objects.filter(user=request.user, box=False, pending=False).count() < 50:
                take_chance = random.randint(1, 8)
                if take_chance != 8:
                    reward = Item.objects.filter(url__icontains="apple").order_by('?').first()
                    message = "You sneakily pull a " + reward.name + " to take home."
                    
                    inventory = Inventory.objects.create(user=request.user, item=reward)
                    claim = DailyClaim.objects.create(user=request.user, daily_type="orchard", message=message, reward=reward)
                    return redirect(apple_orchard_page)
                else:
                    message = "Someone seems to be watching... You decide not to take anything today."
                    claim = DailyClaim.objects.create(user=request.user, daily_type="orchard", message=message)
                    return redirect(apple_orchard_page)
            else:
                request.session['error'] = "You can only have up to 50 items in your inventory."
                return redirect(error_page)
        else:
            request.session['error'] = "You have already taken an apple today."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def day_old_stock_page(request):
    if request.user.is_authenticated():
        today = datetime.today()
        dayold_claim = DailyClaim.objects.filter(user=request.user, daily_type="dayold", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
    else:
        dayold_claim = None
    return render(request, 'world/daily/day_old_stock_page.html', {'dayold_claim':dayold_claim})

def day_old_stock(request):
    if request.user.is_authenticated():
        today = datetime.today()
        dayold_claim = DailyClaim.objects.filter(user=request.user, daily_type="dayold", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
        if dayold_claim == None:
            if Inventory.objects.filter(user=request.user, box=False, pending=False).count() < 50:
                reward = Item.objects.filter(url__icontains="bread").order_by('?').first()
                message = "You are handed a " + reward.name + " to take home."
                
                inventory = Inventory.objects.create(user=request.user, item=reward)
                claim = DailyClaim.objects.create(user=request.user, daily_type="dayold", message=message, reward=reward)
                return redirect(day_old_stock_page)
            else:
                request.session['error'] = "You can only have up to 50 items in your inventory."
                return redirect(error_page)
        else:
            request.session['error'] = "You have already taken something today."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def vending_machine_page(request):
    if request.user.is_authenticated():
        today = datetime.today()
        vend_claim = DailyClaim.objects.filter(user=request.user, daily_type="vend", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day, date_of_claim__hour=today.hour).first()
    else:
        vend_claim = None
    candies = Item.objects.filter(second_category__name="candy")
    return render(request, 'world/daily/vending_machine_page.html', {'vend_claim':vend_claim, 'candies':candies})

def vending_machine(request, pk):
    if request.user.is_authenticated():
        today = datetime.today()
        vend_claim = DailyClaim.objects.filter(user=request.user, daily_type="vend", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day, date_of_claim__hour=today.hour).first()
        if vend_claim == None:
            item = Item.objects.filter(second_category__name="candy", pk=pk).first()
            if item is not None:
                if Inventory.objects.filter(user=request.user, box=False, pending=False).count() < 50:
                    if request.user.profile.points >= 50:
                        request.user.profile.points -= 50
                        request.user.profile.save()
                        message = "You insert some coins and out pops a " + item.name + "."
                        
                        inventory = Inventory.objects.create(user=request.user, item=item)
                        claim = DailyClaim.objects.create(user=request.user, daily_type="vend", message=message, reward=item)
                        return redirect(vending_machine_page)
                    else:
                        request.session['error'] = "You do not have enough points to use the Vending Machine."
                        return redirect(error_page)
                else:
                    request.session['error'] = "You can only have up to 50 items in your inventory."
                    return redirect(error_page)
            else:
                request.session['error'] = "That candy does not exist."
                return redirect(error_page)
        else:
            request.session['error'] = "You have already taken something this hour."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)















