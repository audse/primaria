from django.shortcuts import render, redirect

from datetime import datetime
import random

from ..models import DailyClaim
from shop.models import Item, Category, Inventory
from social.models import Message
from core.models import Pet, Avatar
from utils.error import error_page


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
                            if inventory.item.second_category == Category.objects.get(name="philosophy genre"):
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
