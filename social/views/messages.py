from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from core.views import error_page, profile_page
from social.models import Message


def messages_page(request):
    if request.user.is_authenticated():
        sent_messages = Message.objects.filter(
            sending_user=request.user, deleted_by_sender=False
        ).order_by("-date")
        received_messages = Message.objects.filter(
            receiving_user=request.user, deleted_by_receiver=False
        ).order_by("-date")

        return render(
            request,
            "social/messages_page.html",
            {"sent_messages": sent_messages, "received_messages": received_messages},
        )
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def mark_message_as_read(request, pk):
    if request.user.is_authenticated():
        message = Message.objects.filter(pk=pk).first()
        if message:
            if request.user == message.receiving_user:
                message.read = True
                message.save()
                return redirect(messages_page)
            else:
                request.session[
                    "error"
                ] = "You cannot mark someone else's message as read."
                return redirect(error_page)
        else:
            request.session["error"] = "That message was not found."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def mark_message_as_unread(request, pk):
    if request.user.is_authenticated():
        message = Message.objects.filter(pk=pk).first()
        if message:
            if request.user == message.receiving_user:
                message.read = False
                message.save()
                return redirect(messages_page)
            else:
                request.session[
                    "error"
                ] = "You cannot mark someone else's message as unread."
                return redirect(error_page)
        else:
            request.session["error"] = "That message was not found."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def send_message(request):
    if request.user.is_authenticated():
        receiving_user = request.POST.get("receiving_user")
        subject = request.POST.get("subject")
        text = request.POST.get("text")
        original = request.POST.get("original")

        receiving_user = User.objects.filter(pk=receiving_user).first()
        if request.user not in receiving_user.profile.blocked_users.all():
            if receiving_user:
                if original:
                    original = Message.objects.filter(pk=original).first()
                    if original:
                        message = Message.objects.create(
                            sending_user=request.user,
                            receiving_user=receiving_user,
                            subject=subject,
                            text=text,
                            original_message=original,
                        )
                        return redirect(messages_page)
                    else:
                        request.session[
                            "error"
                        ] = "The message you are replying to was not found."
                        return redirect(error_page)
                else:
                    message = Message.objects.create(
                        sending_user=request.user,
                        receiving_user=receiving_user,
                        subject=subject,
                        text=text,
                    )
                    return redirect(profile_page, username=receiving_user.username)
            else:
                request.session[
                    "error"
                ] = "This user has blocked you. You may not message them."
                return redirect(error_page)
        else:
            request.session["error"] = "No user was found."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def delete_message(request, pk):
    if request.user.is_authenticated():
        message = Message.objects.filter(pk=pk).first()
        if message:
            if request.user == message.receiving_user:
                message.deleted_by_receiver = True
                message.save()
                return redirect(messages_page)
            if request.user == message.sending_user:
                message.deleted_by_sender = True
                message.save()
                return redirect(messages_page)
            else:
                request.session["error"] = "You cannot delete someone else's message."
                return redirect(error_page)
        else:
            request.session[
                "error"
            ] = "You cannot delete a message that does not exist."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)
