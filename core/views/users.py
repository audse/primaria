from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import (
    validate_password,
    password_validators_help_text_html,
)
from datetime import datetime
from datetime import timedelta
from core.models import FriendRequest, Pet, Avatar, Profile
from social.models import Badge, Message
from shop.models import UserShop, Gallery
from utils.error import handle_error, error_page


def profile_page(request, username):
    avatar_count = Avatar.objects.all().count()
    user = User.objects.filter(username=username).first()
    if user:
        pet = Pet.objects.filter(user=user).first()
        badges = Badge.objects.filter(user=user).order_by("rank")
        shop = UserShop.objects.filter(user=user).first()
        gallery = Gallery.objects.filter(user=user).first()
        friends = user.profile.friends.all()

        friend_status = "none"
        sent_friend_request = FriendRequest.objects.filter(
            sending_user=request.user, receiving_user=user
        ).first()
        received_friend_request = FriendRequest.objects.filter(
            receiving_user=request.user, sending_user=user
        ).first()
        if sent_friend_request:
            friend_status = "sent"
        if received_friend_request:
            friend_status = "pending"
        if request.user in user.profile.friends.all():
            friend_status = "friends"

        return render(
            request,
            "core/profile_page.html",
            {
                "user": user,
                "pet": pet,
                "badges": badges,
                "shop": shop,
                "gallery": gallery,
                "avatar_count": avatar_count,
                "friends": friends,
                "friend_status": friend_status,
            },
        )
    else:
        request.session["error"] = (
            "No user with that username (" + username + ") was found."
        )
        return redirect(error_page)


def edit_bio(request):
    if request.user.is_authenticated:
        user = User.objects.filter(username=request.user.username).first()
        if user:
            bio = request.POST.get("bio")
            user.profile.bio = bio
            user.profile.save()
            return redirect(profile_page, request.user.username)
        else:
            request.session["error"] = "No user was found."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def settings_page(request):
    if request.user.is_authenticated:
        confirm = request.session.pop("confirm", False)
        help_text = password_validators_help_text_html()

        return render(
            request,
            "core/settings_page.html",
            {"confirm": confirm, "help_text": help_text},
        )
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def change_password(request):
    if request.user.is_authenticated:
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")
        if new_password == confirm_new_password:
            user = request.user
            try:
                validate_password(new_password)
            except:
                request.session[
                    "error"
                ] = "Password must meet all password requirements."
                return redirect(error_page)
            request.user.set_password(new_password)
            request.user.save()
            user = authenticate(username=user.username, password=new_password)
            auth_login(request, user)
            confirm = request.session[
                "confirm"
            ] = "You have successfully changed your password."
            return redirect(settings_page)
        else:
            request.session[
                "error"
            ] = "New password and confirm new password fields must match."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def change_view_settings(request):
    if request.user.is_authenticated:
        disable_headers = request.POST.get("disable_headers")
        night_mode = request.POST.get("night_mode")
        if disable_headers:
            request.user.profile.disable_header_images = True
        else:
            request.user.profile.disable_header_images = False
        if night_mode:
            request.user.profile.night_mode = True
        else:
            request.user.profile.night_mode = False
        request.user.profile.save()
        return redirect(settings_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def block_user(request, username):
    user = User.objects.filter(username=username).first()

    if not request.user.is_authenticated:
        return (request, "You must be logged in to view this page.")
    if user is None:
        return handle_error(request, "No user with that username was found.")
    if user is request.user:
        return handle_error(request, "You may not block yourself.")

    request.user.profile.blocked_users.add(user)
    request.user.profile.save()

    return redirect(profile_page, username=user.username)


def unblock_user(request, username):
    user = User.objects.filter(username=username).first()

    if not request.user.is_authenticated:
        return handle_error(request, "You must be logged in to view this page.")
    if user is None:
        return handle_error(request, "No user with that username was found.")
    if user not in request.user.profile.blocked_users.all():
        return handle_error(request, "You do not have that user blocked.")

    request.user.profile.blocked_users.remove(user)
    request.user.profile.save()

    return redirect(profile_page, username=user.username)


def users_online_page(request):
    today = datetime.today()
    today = today - timedelta(hours=1)
    users_online = Profile.objects.filter(last_online__gte=today).order_by(
        "-last_online"
    )
    return render(
        request, "core/users_online_page.html", {"users_online": users_online}
    )
