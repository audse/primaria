from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from datetime import datetime
from datetime import timedelta
import random

from shop.models import Item, Category, Inventory
from world.models import DailyClaim

from core.views.static import home_page
from utils.error import handle_error, error_page


def login_page(request):
    if request.user.is_authenticated():
        request.session["error"] = "You are already logged in."
        return redirect(error_page)
    else:
        errors = request.session.pop("errors", False)
        return render(request, "core/login_page.html", {"errors": errors})


def login(request):
    if request.user.is_authenticated():
        request.session["error"] = "You are already logged in."
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
            request.session["errors"] = errors
            return redirect(login_page)


def logout(request):
    auth_logout(request)
    return redirect(home_page)


def claim_login_bonus(request):
    if request.user.is_authenticated():
        today = datetime.today()
        claim = DailyClaim.objects.filter(
            user=request.user,
            daily_type="login",
            date_of_claim__year=today.year,
            date_of_claim__month=today.month,
            date_of_claim__day=today.day,
        ).first()
        if claim is None:
            one_day_ago = today - timedelta(days=1)
            two_days_ago = today - timedelta(days=2)
            three_days_ago = today - timedelta(days=3)
            four_days_ago = today - timedelta(days=4)

            one_day_ago_claim = DailyClaim.objects.filter(
                user=request.user,
                daily_type="login",
                date_of_claim__year=one_day_ago.year,
                date_of_claim__month=one_day_ago.month,
                date_of_claim__day=one_day_ago.day,
            ).first()
            two_days_ago_claim = DailyClaim.objects.filter(
                user=request.user,
                daily_type="login",
                date_of_claim__year=two_days_ago.year,
                date_of_claim__month=two_days_ago.month,
                date_of_claim__day=two_days_ago.day,
            ).first()
            three_days_ago_claim = DailyClaim.objects.filter(
                user=request.user,
                daily_type="login",
                date_of_claim__year=three_days_ago.year,
                date_of_claim__month=three_days_ago.month,
                date_of_claim__day=three_days_ago.day,
            ).first()
            four_days_ago_claim = DailyClaim.objects.filter(
                user=request.user,
                daily_type="login",
                date_of_claim__year=four_days_ago.year,
                date_of_claim__month=four_days_ago.month,
                date_of_claim__day=four_days_ago.day,
            ).first()

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
                reward = (
                    Item.objects.filter(
                        category=Category.objects.get(name="vegetable"), rarity=rarity
                    )
                    | Item.objects.filter(
                        category=Category.objects.get(name="fruit"), rarity=rarity
                    )
                    | Item.objects.filter(
                        category=Category.objects.get(name="junk food"), rarity=rarity
                    )
                    | Item.objects.filter(
                        category=Category.objects.get(name="organic food"),
                        rarity=rarity,
                    )
                )
                reward = reward.order_by("?").first()
                points = None
            elif login_bonus == 3:
                points = 1000
                reward = None
            elif login_bonus == 4:
                rarity = [1, 1, 1, 1, 2, 2, 3]
                rarity = random.choice(rarity)
                reward = (
                    Item.objects.filter(
                        category=Category.objects.get(name="crystal"),
                        name__icontains="small",
                        rarity=rarity,
                    )
                    .order_by("?")
                    .first()
                )
                points = None
            elif login_bonus == 5:
                points = 1500
                reward = None

            if reward:
                # if Inventory.objects.filter(user=request.user, box=False, pending=False).count() >= 50:
                #     request.session['error'] = "You can only have up to 50 items in your inventory."
                #     return redirect(error_page)
                inventory = Inventory.objects.create(user=request.user, item=reward)
                message = (
                    "You have claimed your login bonus and received a "
                    + reward.name
                    + "!"
                )
            else:
                message = (
                    "You have claimed your login bonus and received "
                    + str(points)
                    + " points!"
                )
                request.user.profile.points += points
                request.user.profile.save()
            claim = DailyClaim.objects.create(
                user=request.user,
                daily_type="login",
                reward=reward,
                points=points,
                message=message,
            )
            if login_bonus == 5:
                one_day_ago_claim.delete()
                two_days_ago_claim.delete()
                three_days_ago_claim.delete()
                four_days_ago_claim.delete()
            return redirect(claimed_login_bonus_page)
        else:
            request.session[
                "error"
            ] = "You have already claimed your login bonus for today."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def claimed_login_bonus_page(request):
    if request.user.is_authenticated():
        today = datetime.today()
        claim = DailyClaim.objects.filter(
            user=request.user,
            daily_type="login",
            date_of_claim__year=today.year,
            date_of_claim__month=today.month,
            date_of_claim__day=today.day,
        ).first()
        if claim:
            return render(
                request, "core/features/claimed_login_bonus_page.html", {"claim": claim}
            )
        else:
            request.session["error"] = "You have not yet claimed your login bonus."
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)
