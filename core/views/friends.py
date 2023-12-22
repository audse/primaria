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
from users import profile_page, settings_page


def friends_page(request):
    if not request.user.is_authenticated():
        return handle_error(request, "You must be logged in to view this page.")

    pending_friend_requests = FriendRequest.objects.filter(receiving_user=request.user)
    sent_friend_requests = FriendRequest.objects.filter(sending_user=request.user)
    friends = request.user.profile.friends.all()

    return render(
        request,
        "core/friends_page.html",
        {
            "pending_friend_requests": pending_friend_requests,
            "sent_friend_requests": sent_friend_requests,
            "friends": friends,
        },
    )


def send_friend_request(request, username):
    receiving_user = User.objects.filter(username=username).first()
    note = request.POST.get("note")

    if not request.user.is_authenticated():
        return handle_error(request, "You must be logged in to view this page.")
    if receiving_user is None:
        return handle_error(request, "No user with that username was found.")
    if receiving_user is request.user:
        return handle_error(request, "You may not add yourself as a friend.")
    if receiving_user in request.user.profile.friends.all():
        return handle_error(request, "You are already friends with this user.")
    if (
        request.user in receiving_user.profile.blocked_users.all()
        or request.user.profile.disable_friend_requests
    ):
        return handle_error(
            request, "Sorry, you are unable to send a friend request to this user."
        )

    check_for_previous_request = FriendRequest.objects.filter(
        sending_user__username=request.user.username,
        receiving_user__username=receiving_user.username,
    ).first()
    check_for_pending_request = FriendRequest.objects.filter(
        receiving_user__username=request.user.username,
        sending_user__username=receiving_user.username,
    ).first()
    if check_for_previous_request or check_for_pending_request:
        return handle_error(
            request,
            "You have already sent a friend request to this user (or they have already sent one to you).",
        )

    new_friend_request = FriendRequest.objects.create(
        sending_user=request.user, receiving_user=receiving_user, note=note
    )

    if note:
        text = (
            request.user.username
            + " sent you a friend request with the following note: \n "
            + note
        )
    else:
        text = request.user.username + " sent you a friend request!"

    message = Message.objects.create(
        receiving_user=receiving_user,
        subject="Somebody sent you a friend request!",
        text=text,
    )

    return redirect(friends_page)


def accept_friend_request(request, username):
    requesting_user = User.objects.filter(username=username).first()
    friend_request = FriendRequest.objects.filter(
        sending_user__username=username, receiving_user__username=request.user.username
    ).first()

    if not request.user.is_authenticated():
        return handle_error(request, "You must be logged in to view this page.")
    if requesting_user is None:
        return handle_error(request, "No user with that username was found.")
    if not friend_request:
        return handle_error(request, "That user has not sent you a friend request.")

    request.user.profile.friends.add(requesting_user)
    requesting_user.profile.friends.add(request.user)
    friend_request.delete()

    text = request.user.username + " accepted your friend request. You're now friends!"
    message = Message.objects.create(
        receiving_user=requesting_user,
        subject="Someone accepted your friend request!",
        text=text,
    )

    return redirect(friends_page)


def reject_friend_request(request, username):
    requesting_user = User.objects.filter(username=username).first()
    friend_request = FriendRequest.objects.filter(
        sending_user__username=username, receiving_user__username=request.user.username
    ).first()

    if not request.user.is_authenticated():
        return handle_error(request, "You must be logged in to view this page.")
    if requesting_user is None:
        return handle_error(request, "No user with that username was found.")
    if not friend_request:
        return handle_error(request, "That user has not sent you a friend request.")

    friend_request.delete()

    text = request.user.username + " rejected your friend request."
    message = Message.objects.create(
        receiving_user=requesting_user,
        subject="Someone rejected your friend request.",
        text=text,
    )

    return redirect(friends_page)


def remove_friend(request, username):
    user_to_remove = User.objects.filter(username=username).first()

    if not request.user.is_authenticated():
        return handle_error(request, "You must be logged in to view this page.")
    if user_to_remove is None:
        return handle_error(request, "No user with that username was found.")

    request.user.profile.friends.remove(user_to_remove)
    user_to_remove.profile.friends.remove(request.user)

    return redirect(friends_page)


def change_friend_request_settings(request):
    friend_request_settings = request.POST.get("friend_request_settings")

    if not request.user.is_authenticated():
        return handle_error(request, "You must be logged in to view this page.")

    if not friend_request_settings:
        friend_request_settings = False

    request.user.profile.disable_friend_requests = friend_request_settings
    request.user.profile.save()

    return redirect(settings_page)
