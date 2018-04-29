from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html
from datetime import datetime
from datetime import timedelta
import random

from .models import Pet, Animal, Avatar, Profile
from social.models import Badge, Message, Board, Topic
from shop.models import UserShop, Gallery, Item, Category, Inventory
from world.models import DailyClaim

def home_page(request):
    announcements = Topic.objects.filter(board=Board.objects.get(name="Announcements")).order_by('-date')[:5]
    return render(request, 'core/home_page.html', {'announcements':announcements})

def privacy_policy_page(request):
    return render(request, 'core/privacy_policy_page.html')

def error_page(request):
    error = request.session.pop('error', False)
    if error == False:
        error = "We are not sure what, but we will work on fixing it."
    return render(request, 'core/error_page.html', {'error':error})

def profile_page(request, username):
    avatar_count = Avatar.objects.all().count()
    user = User.objects.filter(username=username).first()
    if user:
        pet = Pet.objects.filter(user=user).first()
        badges = Badge.objects.filter(user=user).order_by('rank')
        shop = UserShop.objects.filter(user=user).first()
        gallery = Gallery.objects.filter(user=user).first()
        return render(request, 'core/profile_page.html', {'user':user, 'pet':pet, 'badges':badges, 'shop':shop, 'gallery':gallery, 'avatar_count':avatar_count})
    else:
        request.session['error'] = "No user with that username ("+username+") was found."
        return redirect(error_page)

def edit_bio(request):
    if request.user.is_authenticated():
        user = User.objects.filter(username=request.user.username).first()
        if user:
            bio = request.POST.get("bio")
            user.profile.bio = bio
            user.profile.save()
            return redirect(profile_page, request.user.username)
        else:
            request.session['error'] = "No user was found."
            return redirect(error_page)
    else:
        request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def register_page(request):
    if request.user.is_authenticated():
        request.session['error'] = "You are already registered."
        return redirect(error_page)
    else:
        help_text = password_validators_help_text_html()
        errors = request.session.pop('errors', False)
        return render(request, 'core/register_page.html', {'help_text':help_text, 'errors':errors})

def successful_register_page(request):
    return render(request, 'core/successful_register_page.html')

def register(request):
    if request.user.is_authenticated():
        request.session['error'] = "You are already registered."
        return redirect(error_page)
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        # email = request.POST.get("email")
        age = request.POST.get("age")

        errors = []

        if not username or not password or not confirm_password:
            errors.append("All fields must be filled out.")
        else:
            if not age:
                errors.append("You must be 13 years or older to join.")

        if password != confirm_password:
            errors.append("Passwords do not match.")

        # if email:
        #     if "@" not in email or "." not in email:
        #         errors.append("Email is not valid.")

        if len(password) < 8:
            errors.append("Your password must be at least 8 characters.")
        try:
            password = int(password)
            errors.append("Your password cannot be entirely numeric.")
        except:
            pass

        username_taken = User.objects.filter(username=username).first()
        if username_taken is not None:
            errors.append("Sorry, that username has been taken.")

        # validate_password(password).messages

        try:
            validate_password(password)
        except:
            errors.append("That password is either too common, or too similar to your username.")

        if not errors:

            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()

            # AVATARS #
            user = User.objects.get(username=username)
            new_avatar = Avatar.objects.get(url="hi-im-new")
            user.profile.avatars.add(new_avatar)
            user.profile.save()

            subject = "You just found an avatar!"
            text = "You have just received the avatars \"" + new_avatar.name + "\" to use on the boards! It has been set as your default."
            message = Message.objects.create(receiving_user=user, subject=subject, text=text)

            return redirect(successful_register_page)
        else:
            request.session['errors'] = errors
            return redirect(register_page)

def login_page(request):
    if request.user.is_authenticated():
        request.session['error'] = "You are already logged in."
        return redirect(error_page)
    else:
        errors = request.session.pop('errors', False)
        return render(request, 'core/login_page.html', {'errors':errors})

def login(request):
    if request.user.is_authenticated():
        request.session['error'] = "You are already logged in."
        return redirect(error_page)
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        errors = []

        if not username or not password:
            errors.append("All fields must be filled out.")
        else:
            user_exists = User.objects.filter(username=username).first()
            if user_exists is not None:
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                else:
                    errors.append("Username and password do not match.")
            else:
                errors.append("User does not exist.")

        if not errors:
            return redirect(home_page)
        else:
            request.session['errors'] = errors
            return redirect(login_page)

def logout(request):
    auth_logout(request)
    return redirect(home_page)

def settings_page(request):
    if request.user.is_authenticated():
        confirm = request.session.pop('confirm', False)
        help_text = password_validators_help_text_html()

        return render(request, 'core/settings_page.html', {'confirm':confirm, 'help_text':help_text})
    else:
        error = request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def change_password(request):
    if request.user.is_authenticated():
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        if new_password == confirm_new_password:
            user = request.user
            try:
                validate_password(new_password)
            except:
                error = request.session['error'] = "Password must meet all password requirements."
                return redirect(error_page)  
            request.user.set_password(new_password)
            request.user.save()
            user = authenticate(username=user.username, password=new_password)
            auth_login(request, user)
            confirm = request.session['confirm'] = "You have successfully changed your password."
            return redirect(settings_page)
        else:
            error = request.session['error'] = "New password and confirm new password fields must match."
            return redirect(error_page)
    else:
        error = request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def change_view_settings(request):
    if request.user.is_authenticated():
        disable_headers = request.POST.get("disable_headers")
        if disable_headers:
            request.user.profile.disable_header_images = True
        else:
            request.user.profile.disable_header_images = False
        request.user.profile.save()
        return redirect(settings_page)
    else:
        error = request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def create_pet_step_1(request):
    pet = Pet.objects.filter(user=request.user).first()
    if pet is None:
        animals = Animal.objects.all().order_by('name')
        return render(request, 'core/features/create_pet_step_1.html', {'animals':animals})
    else:
        error = request.session['error'] = "You can't create another pet when you already have one."
        return redirect(error_page)

def create_pet_step_2(request, animal):
    pet = Pet.objects.filter(user=request.user).first()
    if pet is None:
        animal = Animal.objects.get(name=animal)
        return render(request, 'core/features/create_pet_step_2.html', {'animal':animal})
    else:
        error = request.session['error'] = "You can't create another pet when you already have one."
        return redirect(error_page)

def create_pet_step_3(request, animal):
    pet = Pet.objects.filter(user=request.user).first()
    if pet is None:
        animal = Animal.objects.get(name=animal)
        color = request.POST.get("color")
        if color == "red" or color == "yellow" or color == "green" or color == "blue" or color == "black":
            error = request.session.pop('error', False)
            if error:
                color = request.session.pop('color', False)
            return render(request, 'core/features/create_pet_step_3.html', {'animal':animal, 'color':color, 'error':error})
        else:
            request.session['error'] = "No cheating, please! That ruins the fun for everyone."
            return redirect(error_page)
    else:
        error = request.session['error'] = "You can't create another pet when you already have one."
        return redirect(error_page)

def create_pet(request):
    if request.user.is_authenticated():
        pet = Pet.objects.filter(user=request.user).first()
        if pet is None:
            animal = request.POST.get("animal")
            color = request.POST.get("color")
            name = request.POST.get("name")

            check_unique = Pet.objects.filter(name=name).first()
            if check_unique is not None:
                error = "Sorry, that name is already taken."
                request.session['error'] = error
                request.session['color'] = color
                return redirect(create_pet_step_3, animal)
            else:
                if color == "red" or color == "yellow" or color == "green" or color == "blue" or color == "black":
                    if animal == "dino" or animal == "lizard" or animal == "monkey" or animal == "mouse" or animal == "tapir":
                        animal = Animal.objects.get(name=animal)
                        all_colors = color + " " + animal.name + ","
                        pet = Pet.objects.create(user=request.user, animal=animal, color=color, name=name, all_colors=all_colors)
                        
                        # AVATARS
                        pet_avatar = Avatar.objects.get(url=animal.name)
                        color_avatar = Avatar.objects.get(url=color)
                        request.user.profile.avatars.add(pet_avatar)
                        request.user.profile.avatars.add(color_avatar)
                        request.user.profile.save()

                        subject = "You just found some avatars!"
                        text = "You have just received the avatars \"" + pet_avatar.name + "\" and \"" + color_avatar.name + "\" to use on the boards!"
                        message = Message.objects.create(receiving_user=request.user, subject=subject, text=text)

                        return redirect(successful_create_pet_page)
                    else:
                        request.session['error'] = "No cheating, please! That ruins the fun for everyone."
                        return redirect(error_page)
                else:
                    request.session['error'] = "No cheating, please! That ruins the fun for everyone."
                    return redirect(error_page)
        else:
            error = request.session['error'] = "You can't create another pet when you already have one."
            return redirect(error_page)
    else:
        error = request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def successful_create_pet_page(request):
    return render(request, 'core/features/successful_create_pet_page.html')

def change_pet_page(request):
    if request.user.is_authenticated():
        pet = Pet.objects.filter(user=request.user).first()
        if pet:

            # AVATARS
            red = Avatar.objects.get(url="red")
            yellow = Avatar.objects.get(url="yellow")
            green = Avatar.objects.get(url="green")
            blue = Avatar.objects.get(url="blue")
            black = Avatar.objects.get(url="black")

            dino = Avatar.objects.get(url="dino")
            lizard = Avatar.objects.get(url="lizard")
            monkey = Avatar.objects.get(url="monkey")
            mouse = Avatar.objects.get(url="mouse")
            tapir = Avatar.objects.get(url="tapir")

            color_avatars = [red, yellow, green, blue, black]
            animal_avatars = [dino, lizard, monkey, mouse, tapir]

            for avatar in color_avatars:
                color = avatar.url
                if "dino "+color in pet.all_colors and "lizard"+color in pet.all_colors and "monkey "+color in pet.all_colors and "mouse "+color in pet.all_colors and "tapir"+color in pet.all_colors:
                    if avatar not in request.user.profile.avatars.all():
                        request.user.profile.avatars.add(avatar)
                        request.user.profile.save()
                        message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"" + avatar.name + "\" to use on the boards!")

            for avatar in animal_avatars:
                animal = avatar.url
                if animal+" red" in pet.all_colors and animal+" yellow" in pet.all_colors and animal+" green" in pet.all_colors and animal+" blue" in pet.all_colors and animal+" black" in pet.all_colors:
                    if avatar not in request.user.profile.avatars.all():
                        request.user.profile.avatars.add(avatar)
                        request.user.profile.save()
                        message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"" + avatar.name + "\" to use on the boards!")

            rainbow_avatar = Avatar.objects.get(url="rainbow")
            if rainbow_avatar not in request.user.profile.avatars.all():
                if "red" in pet.all_colors and "yellow" in pet.all_colors and "green" in pet.all_colors and "blue" in pet.all_colors and "black" in pet.all_colors:
                    all_colors_count = len(pet.all_colors.split(",").pop())
                    if all_colors_count >= 10:
                        request.user.profile.avatars.add(rainbow_avatar)
                        request.user.profile.save()
                        message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"" + rainbow_avatar.name + "\" to use on the boards!")

            all_colors = pet.all_colors.split(",")
            for n in range(0, len(all_colors)-1):
                all_colors[n] = all_colors[n].split(" ")
                n += 1
            all_colors = tuple(all_colors)

            return render(request, 'core/change_pet_page.html', {'all_colors': all_colors})
        else:
            error = request.session['error'] = "You must have a pet to view this page."
            return redirect(error_page)
    else:
        error = request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def change_pet(request):
    if request.user.is_authenticated():
        pet = Pet.objects.filter(user=request.user).first()
        if pet:
            new_color = request.POST.get("color")
            new_animal = request.POST.get("animal")
            string = new_color + " " + new_animal + ","
            if string in pet.all_colors:
                new_animal = Animal.objects.filter(name=new_animal).first()
                if new_animal:
                    pet.color = new_color
                    pet.animal = new_animal
                    pet.save()
                    return redirect(change_pet_page)
                else:
                    error = request.session['error'] = "That animal does not exist."
                    return redirect(error_page)
            else:
                error = request.session['error'] = "You cannot make a pet a color you haven't unlocked."
                return redirect(error_page)
        else:
            error = request.session['error'] = "You must have a pet to view this page."
            return redirect(error_page)
    else:
        error = request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def colors_page(request):
    return render(request, 'core/features/colors_page.html')

def rules_page(request):
    return render(request, 'core/rules_page.html')

def block_user(request, username):
    if request.user.is_authenticated():
        user = User.objects.filter(username=username).first()
        if user != None:
            if user != request.user:
                request.user.profile.blocked_users.add(user)
                request.user.profile.save()
                return redirect(profile_page, username=user.username)
            else:
                error = request.session['error'] = "You may not block yourself."
                return redirect(error_page)
        else:
            error = request.session['error'] = "No user with that username was found."
            return redirect(error_page)
    else:
        error = request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def unblock_user(request, username):
    if request.user.is_authenticated():
        user = User.objects.filter(username=username).first()
        if user != None:
            if user in request.user.profile.blocked_users.all():
                request.user.profile.blocked_users.remove(user)
                request.user.profile.save()
                return redirect(profile_page, username=user.username)
            else:
                error = request.session['error'] = "You do not have that user blocked."
                return redirect(error_page)
        else:
            error = request.session['error'] = "No user with that username was found."
            return redirect(error_page)
    else:
        error = request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def users_online_page(request):
    today = datetime.today()
    today = today - timedelta(hours=1)
    users_online = Profile.objects.filter(last_online__year=today.year, last_online__month=today.month, last_online__day=today.day, last_online__hour__gte=today.hour).order_by('-last_online')
    return render(request, 'core/users_online_page.html', {'users_online':users_online})

def claim_login_bonus(request):
    if request.user.is_authenticated():
        today = datetime.today()
        claim = DailyClaim.objects.filter(user=request.user, daily_type="login", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
        if claim is None:
            one_day_ago = today - timedelta(days=1)
            two_days_ago = today - timedelta(days=2)
            three_days_ago = today - timedelta(days=3)
            four_days_ago = today - timedelta(days=4)

            one_day_ago_claim = DailyClaim.objects.filter(user=request.user, daily_type="login", date_of_claim__year=one_day_ago.year, date_of_claim__month=one_day_ago.month, date_of_claim__day=one_day_ago.day).first()
            two_days_ago_claim = DailyClaim.objects.filter(user=request.user, daily_type="login", date_of_claim__year=two_days_ago.year, date_of_claim__month=two_days_ago.month, date_of_claim__day=two_days_ago.day).first()
            three_days_ago_claim = DailyClaim.objects.filter(user=request.user, daily_type="login", date_of_claim__year=three_days_ago.year, date_of_claim__month=three_days_ago.month, date_of_claim__day=three_days_ago.day).first()
            four_days_ago_claim = DailyClaim.objects.filter(user=request.user, daily_type="login", date_of_claim__year=four_days_ago.year, date_of_claim__month=four_days_ago.month, date_of_claim__day=four_days_ago.day).first()

            login_bonus = 1
            if one_day_ago_claim != None:
                login_bonus = 2
                if two_days_ago_claim != None:
                    login_bonus = 3
                    if three_days_ago_claim != None:
                        login_bonus = 4
                        if four_days_ago_claim != None:
                            login_bonus = 5
                            
            if login_bonus == 1:
                points = 500
                reward = None
            elif login_bonus == 2:
                rarity = [1, 1, 1, 1, 2, 2, 3]
                rarity = random.choice(rarity)
                reward = Item.objects.filter(category=Category.objects.get(name="vegetable"), rarity=rarity) | Item.objects.filter(category=Category.objects.get(name="fruit"), rarity=rarity) | Item.objects.filter(category=Category.objects.get(name="junk food"), rarity=rarity) | Item.objects.filter(category=Category.objects.get(name="organic food"), rarity=rarity)
                reward = reward.order_by('?').first()
                points = None
            elif login_bonus == 3:
                points = 1000
                reward = None
            elif login_bonus == 4:
                rarity = [1, 1, 1, 1, 2, 2, 3]
                rarity = random.choice(rarity)
                reward = Item.objects.filter(category=Category.objects.get(name="crystal"), name__icontains="small", rarity=rarity).order_by('?').first()
                points = None
            elif login_bonus == 5:
                points = 1500
                reward = None

            if reward:
                if Inventory.objects.filter(user=request.user, box=False, pending=False).count() >= 50:
                    error = request.session['error'] = "You can only have up to 50 items in your inventory."
                    return redirect(error_page)
                inventory = Inventory.objects.create(user=request.user, item=reward)
                message = "You have claimed your login bonus and recieved a " + reward.name + "!"
            else:
                message = "You have claimed your login bonus and recieved " + str(points) + " points!"
                request.user.profile.points += points
                request.user.profile.save()
            claim = DailyClaim.objects.create(user=request.user, daily_type="login", reward=reward, points=points, message=message)
            if login_bonus == 5:
                one_day_ago_claim.delete()
                two_days_ago_claim.delete()
                three_days_ago_claim.delete()
                four_days_ago_claim.delete()
            return redirect(claimed_login_bonus_page)
        else:
            error = request.session['error'] = "You have already claimed your login bonus for today."
            return redirect(error_page)
    else:
        error = request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)

def claimed_login_bonus_page(request):
    if request.user.is_authenticated():
        today = datetime.today()
        claim = DailyClaim.objects.filter(user=request.user, daily_type="login", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
        if claim:
            return render(request, 'core/features/claimed_login_bonus_page.html', {'claim':claim})
        else:
            error = request.session['error'] = "You have not yet claimed your login bonus."
    else:
        error = request.session['error'] = "You must be logged in to view this page."
        return redirect(error_page)





