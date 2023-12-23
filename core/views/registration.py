from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import (
    validate_password,
    password_validators_help_text_html,
)
from core.models import Avatar
from social.models import Message
from utils.error import error_page


def register_page(request):
    if request.user.is_authenticated:
        request.session["error"] = "You are already registered."
        return redirect(error_page)
    else:
        help_text = password_validators_help_text_html()
        errors = request.session.pop("errors", False)
        return render(
            request,
            "core/register_page.html",
            {"help_text": help_text, "errors": errors},
        )


def successful_register_page(request):
    return render(request, "core/successful_register_page.html")


def register(request):
    if request.user.is_authenticated:
        request.session["error"] = "You are already registered."
        return redirect(error_page)
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        age = request.POST.get("age")

        errors = []

        if not username or not password or not confirm_password:
            errors.append("All fields must be filled out.")
        else:
            if not age:
                errors.append("You must be 13 years or older to join.")

        if password != confirm_password:
            errors.append("Passwords do not match.")

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

        try:
            validate_password(password)
        except:
            errors.append(
                "That password is either too common, or too similar to your username."
            )

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
            text = (
                'You have just received the avatars "'
                + new_avatar.name
                + '" to use on the boards! It has been set as your default.'
            )
            message = Message.objects.create(
                receiving_user=user, subject=subject, text=text
            )

            return redirect(successful_register_page)
        else:
            request.session["errors"] = errors
            return redirect(register_page)
