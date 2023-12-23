from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from core.views import error_page
from social.models import Message, Board, Topic, Reply
from core.models import Pet, Avatar
import random
from django.utils import timezone


def boards_page(request):
    boards = Board.objects.all()
    for board in boards:
        board.last_topic = (
            Topic.objects.filter(board=board, deleted=False).order_by("-date").first()
        )
        if board.last_topic is not None:
            board.last_topic = board.last_topic.date
        else:
            board.last_topic = "N/A"
    return render(request, "social/boards_page.html", {"boards": boards})


def board_page(request, board):
    board = Board.objects.filter(url=board).first()
    if board:
        topics = Topic.objects.filter(
            board=board, deleted=False, sticky=False
        ).order_by("-last_reply_date")
        sticky_topics = Topic.objects.filter(
            board=board, deleted=False, sticky=True
        ).order_by("-last_reply_date")

        for topic in sticky_topics:
            replies = Reply.objects.filter(topic=topic).order_by("-date")
            last_reply = replies.last()
            if last_reply:
                topic.last_reply = last_reply.date
            else:
                topic.last_reply = topic.date
            topic.replies = replies.count()

        for topic in topics:
            replies = Reply.objects.filter(topic=topic).order_by("-date")
            last_reply = replies.last()
            if last_reply:
                topic.last_reply = last_reply.date
            else:
                topic.last_reply = topic.date
            topic.replies = replies.count()

        paginator = Paginator(topics, 15)
        page = request.GET.get("page")

        if page:
            try:
                page = int(page)
            except:
                request.session["error"] = "Page must be a number."
                return redirect(error_page)
            topics = paginator.page(page)
        else:
            topics = paginator.page(1)

        return render(
            request,
            "social/board_page.html",
            {"board": board, "topics": topics, "sticky_topics": sticky_topics},
        )
    else:
        request.session["error"] = "No board with that name exists."
        return redirect(error_page)


def topic_page(request, topic):
    topic = Topic.objects.filter(slug=topic).first()
    if topic:
        replies = Reply.objects.filter(topic=topic).order_by("date")
        paginator = Paginator(replies, 10)
        page = request.GET.get("page")
        if page:
            try:
                page = int(page)
            except:
                request.session["error"] = "Page must be an integer."
                return redirect(error_page)
            replies = paginator.page(page)
        else:
            replies = paginator.page(1)

        pet = Pet.objects.filter(user=topic.user).first()
        if pet:
            topic.pet = pet
        return render(
            request, "social/topic_page.html", {"topic": topic, "replies": replies}
        )
    else:
        request.session["error"] = "No topic with that name exists."
        return redirect(error_page)


def change_avatar(request, avatar):
    if request.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(url=avatar)
        except:
            request.session["error"] = "That avatar does not exist."
            return redirect(error_page)

        if avatar in request.user.profile.avatars.all():
            request.user.profile.selected_avatar = avatar.url
            request.user.profile.save()
            return redirect(boards_page)
        else:
            request.session["error"] = "You have not unlocked that avatar."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def post_topic(request):
    if request.user.is_authenticated:
        board = request.POST.get("board")
        title = request.POST.get("title")
        message = request.POST.get("message")
        if board:
            try:
                board = int(board)
            except:
                request.session["error"] = "Board ID must be an integer."
                return redirect(error_page)
            board = Board.objects.filter(pk=board).first()
            if board:
                if message and title:
                    if (board.staff and request.user.is_staff) or (
                        board.staff == False
                    ):
                        topic = Topic.objects.create(
                            user=request.user, board=board, title=title, message=message
                        )
                        return redirect(topic_page, topic.slug)
                    else:
                        request.session[
                            "error"
                        ] = "You must be a staff member to post a topic to that board."
                        return redirect(error_page)
                else:
                    request.session[
                        "error"
                    ] = "Topic message and title cannot be blank."
                    return redirect(error_page)
            else:
                request.session["error"] = "That topic does not exist."
                return redirect(error_page)
        else:
            request.session["error"] = "You must post a topic to a board."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def reply_to_topic(request):
    if request.user.is_authenticated:
        topic = request.POST.get("topic")
        message = request.POST.get("message")
        if topic:
            try:
                topic = int(topic)
            except:
                request.session["error"] = "Topic ID must be an integer."
                return redirect(error_page)
            topic = Topic.objects.filter(pk=topic).first()
            if topic:
                if not topic.locked:
                    if message:
                        reply = Reply.objects.create(
                            user=request.user, topic=topic, message=message
                        )
                        topic.last_reply_date = timezone.now()
                        topic.save()

                        # AVATARS
                        chatty_avatar = Avatar.objects.get(url="very-chatty")
                        if chatty_avatar not in request.user.profile.avatars.all():
                            replies = Reply.objects.filter(user=request.user).count()
                            if replies == 100:
                                request.user.profile.avatars.add(chatty_avatar)
                                request.user.profile.save()
                                message = Message.objects.create(
                                    receiving_user=request.user,
                                    subject="You just found a secret avatar!",
                                    text='You have just received the avatar "Very Chatty" to use on the boards!',
                                )

                        if random.randint(1, 4) == 1:
                            big_avatar = Avatar.objects.get(url="big-if-true")
                            if big_avatar not in request.user.profile.avatars.all():
                                if topic.board == Board.objects.get(
                                    url="announcements"
                                ):
                                    request.user.profile.avatars.add(big_avatar)
                                    request.user.profile.save()
                                    message = Message.objects.create(
                                        receiving_user=request.user,
                                        subject="You just found a secret avatar!",
                                        text='You have just received the avatar "Big If True" to use on the boards!',
                                    )

                        return redirect(topic_page, topic.slug)
                    else:
                        request.session["error"] = "Reply message cannot be blank."
                        return redirect(error_page)
                else:
                    request.session[
                        "error"
                    ] = "You may not reply to a topic that is locked."
                    return redirect(error_page)
            else:
                request.session["error"] = "That topic does not exist."
                return redirect(error_page)
        else:
            request.session["error"] = "You must reply to a topic."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def lock_topic(request, topic):
    if request.user.is_authenticated and request.user.is_staff:
        topic = Topic.objects.filter(slug=topic).first()
        topic.locked = True
        topic.save()
        return redirect(topic_page, topic.slug)
    else:
        request.session["error"] = "You must be a staff member to view this page."
        return redirect(error_page)


def unlock_topic(request, topic):
    if request.user.is_authenticated and request.user.is_staff:
        topic = Topic.objects.filter(slug=topic).first()
        topic.locked = False
        topic.save()
        return redirect(topic_page, topic.slug)
    else:
        request.session["error"] = "You must be a staff member to view this page."
        return redirect(error_page)


def delete_topic(request, topic):
    if request.user.is_authenticated and request.user.is_staff:
        topic = Topic.objects.filter(slug=topic).first()
        topic.deleted = True
        topic.save()
        message = Message.objects.create(
            receiving_user=topic.user,
            subject="Your Topic Has Been Deleted",
            text="Your topic has been deleted. Please refer to the site rules before posting a topic.",
        )
        return redirect(topic_page, topic.slug)
    else:
        request.session["error"] = "You must be a staff member to view this page."
        return redirect(error_page)


def undelete_topic(request, topic):
    if request.user.is_authenticated and request.user.is_staff:
        topic = Topic.objects.filter(slug=topic).first()
        topic.deleted = False
        topic.save()
        return redirect(topic_page, topic.slug)
    else:
        request.session["error"] = "You must be a staff member to view this page."
        return redirect(error_page)


def sticky_topic(request, topic):
    if request.user.is_authenticated and request.user.is_staff:
        topic = Topic.objects.filter(slug=topic).first()
        topic.sticky = True
        topic.save()
        return redirect(topic_page, topic.slug)
    else:
        request.session["error"] = "You must be a staff member to view this page."
        return redirect(error_page)


def unsticky_topic(request, topic):
    if request.user.is_authenticated and request.user.is_staff:
        topic = Topic.objects.filter(slug=topic).first()
        topic.sticky = False
        topic.save()
        return redirect(topic_page, topic.slug)
    else:
        request.session["error"] = "You must be a staff member to view this page."
        return redirect(error_page)


def delete_reply(request):
    if request.user.is_authenticated and request.user.is_staff:
        reply = request.POST.get("reply")
        deleted_reason = request.POST.get("deleted_reason")
        reply = Reply.objects.filter(pk=reply).first()
        reply.deleted = True
        reply.deleted_reason = deleted_reason
        reply.save()
        message = Message.objects.create(
            receiving_user=reply.user,
            subject="Your Reply Has Been Deleted",
            text='Your reply has been deleted, for the reason: "'
            + deleted_reason
            + '". Please refer to the site rules before posting a reply.',
        )
        return redirect(topic_page, reply.topic.slug)
    else:
        request.session["error"] = "You must be a staff member to view this page."
        return redirect(error_page)


def undelete_reply(request, reply):
    if request.user.is_authenticated and request.user.is_staff:
        reply = Reply.objects.filter(pk=reply).first()
        reply.deleted = False
        reply.deleted_reason = None
        reply.save()
        return redirect(topic_page, reply.topic.slug)
    else:
        request.session["error"] = "You must be a staff member to view this page."
        return redirect(error_page)
