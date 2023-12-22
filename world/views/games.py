from django.shortcuts import render, redirect

from datetime import datetime

from ..models import Score
from shop.models import Item, Inventory
from social.models import Message, Badge
from core.models import Avatar
from utils.error import error_page


def games_page(request):
    return render(request, "world/games_page.html")


def blackjack_page(request):
    today = datetime.today()
    if request.user.is_authenticated():
        scores_sent = Score.objects.filter(
            user=request.user,
            game="blackjack",
            date__year=today.year,
            date__month=today.month,
            date__day=today.day,
        ).count()
    else:
        scores_sent = 0
    return render(request, "world/blackjack_page.html", {"scores_sent": scores_sent})


def tictactoe_page(request):
    today = datetime.today()
    if request.user.is_authenticated():
        scores_sent = Score.objects.filter(
            user=request.user,
            game="tictactoe",
            date__year=today.year,
            date__month=today.month,
            date__day=today.day,
        ).count()
    else:
        scores_sent = 0
    return render(request, "world/tictactoe_page.html", {"scores_sent": scores_sent})


def pyramids_page(request):
    today = datetime.today()
    if request.user.is_authenticated():
        scores_sent = Score.objects.filter(
            user=request.user,
            game="pyramids",
            date__year=today.year,
            date__month=today.month,
            date__day=today.day,
        ).count()
    else:
        scores_sent = 0
    return render(request, "world/pyramids_page.html", {"scores_sent": scores_sent})


def wheel_serendipity_page(request):
    today = datetime.today()
    if request.user.is_authenticated():
        score = Score.objects.filter(
            user=request.user,
            game="serendipity",
            date__year=today.year,
            date__month=today.month,
            date__day=today.day,
        ).first()
    else:
        score = None
    return render(request, "world/wheel_serendipity_page.html", {"score": score})


def wheel_plush_page(request):
    today = datetime.today()
    if request.user.is_authenticated():
        score = Score.objects.filter(
            user=request.user,
            game="plush",
            date__year=today.year,
            date__month=today.month,
            date__day=today.day,
        ).first()
    else:
        score = None
    return render(request, "world/wheel_plush_page.html", {"score": score})


def send_score(request, game):
    if request.user.is_authenticated():
        if request.POST.get("score") == "success":
            today = datetime.today()
            scores_sent = Score.objects.filter(
                user=request.user,
                game=game,
                date__year=today.year,
                date__month=today.month,
                date__day=today.day,
            ).count()

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
                    message = Message.objects.create(
                        receiving_user=request.user, subject=subject, text=text
                    )
                    badge = Badge.objects.create(
                        user=request.user, rank="amateur", area="gamer"
                    )
                elif all_scores == 1000:
                    subject = "Congratulations!"
                    text = "You have just reached 1,000 total scores sent in games! You have been awarded the Professional Gamer Badge."
                    message = Message.objects.create(
                        receiving_user=request.user, subject=subject, text=text
                    )
                    badge = Badge.objects.create(
                        user=request.user, rank="professional", area="gamer"
                    )
                elif all_scores == 3000:
                    subject = "Congratulations!"
                    text = "You have just reached 3000 total scores sent in games! You have been awarded the Expert Gamer Badge."
                    message = Message.objects.create(
                        receiving_user=request.user, subject=subject, text=text
                    )
                    badge = Badge.objects.create(
                        user=request.user, rank="expert", area="gamer"
                    )

                if game == "blackjack":
                    return redirect(blackjack_page)
                elif game == "tictactoe":
                    return redirect(tictactoe_page)
            else:
                error = "You've already sent the maximum scores for this game today."
                request.session["error"] = error
                return redirect(error_page)
        elif request.POST.get("score") is None:
            # AVATARS
            cheat_avatar = Avatar.objects.get(url="pumpkin-eater")
            if cheat_avatar not in request.user.profile.avatars.all():
                request.user.profile.avatars.add(cheat_avatar)
                request.user.profile.save()
                message = Message.objects.create(
                    receiving_user=request.user,
                    subject="You just found a secret avatar!",
                    text='You have just received the avatar "Pumpkin-Eater" to use on the boards!',
                )

            error = "No cheating, please! That ruins the fun for everyone."
            request.session["error"] = error
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
                        message = Message.objects.create(
                            receiving_user=request.user,
                            subject="You just found a secret avatar!",
                            text='You have just received the avatar "Pumpkin-Eater" to use on the boards!',
                        )

                    error = "No cheating, please! That ruins the fun for everyone."
                    request.session["error"] = error
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
                    message = Message.objects.create(
                        receiving_user=request.user,
                        subject="You just found a secret avatar!",
                        text='You have just received the avatar "Pumpkin-Eater" to use on the boards!',
                    )

                error = "No cheating, please! That ruins the fun for everyone."
                request.session["error"] = error
                return redirect(error_page)
            elif game == "serendipity" and score > 3000:
                # AVATARS
                cheat_avatar = Avatar.objects.get(url="pumpkin-eater")
                if cheat_avatar not in request.user.profile.avatars.all():
                    request.user.profile.avatars.add(cheat_avatar)
                    request.user.profile.save()
                    message = Message.objects.create(
                        receiving_user=request.user,
                        subject="You just found a secret avatar!",
                        text='You have just received the avatar "Pumpkin-Eater" to use on the boards!',
                    )

                error = "No cheating, please! That ruins the fun for everyone."
                request.session["error"] = error
                return redirect(error_page)
            elif game == "plush" and score not in [0, 1]:
                # AVATARS
                cheat_avatar = Avatar.objects.get(url="pumpkin-eater")
                if cheat_avatar not in request.user.profile.avatars.all():
                    request.user.profile.avatars.add(cheat_avatar)
                    request.user.profile.save()
                    message = Message.objects.create(
                        receiving_user=request.user,
                        subject="You just found a secret avatar!",
                        text='You have just received the avatar "Pumpkin-Eater" to use on the boards!',
                    )

                error = "No cheating, please! That ruins the fun for everyone."
                request.session["error"] = error
                return redirect(error_page)
            else:
                today = datetime.today()
                scores_sent = Score.objects.filter(
                    user=request.user,
                    game=game,
                    date__year=today.year,
                    date__month=today.month,
                    date__day=today.day,
                ).count()

                scores_sendable = 0
                if game == "pyramids":
                    scores_sendable = 4
                elif game == "serendipity":
                    scores_sendable = 1
                elif game == "plush":
                    scores_sendable = 1

                if scores_sent < scores_sendable:
                    if game == "plush" and score == 1:
                        item = (
                            Item.objects.filter(category__name="plush", rarity=1)
                            .order_by("?")
                            .first()
                        )
                        if (
                            Inventory.objects.filter(
                                user=request.user, box=False, pending=False
                            ).count()
                            < 50
                        ):
                            inventory = Inventory.objects.create(
                                user=request.user, item=item
                            )
                            # score = 0
                            new_score = Score.objects.create(
                                user=request.user, game=game, score=score
                            )
                            return redirect(wheel_plush_page)
                        else:
                            request.session[
                                "error"
                            ] = "You can only have up to 50 items in your inventory."
                            return redirect(error_page)
                    else:
                        new_score = Score.objects.create(
                            user=request.user, game=game, score=score
                        )

                        request.user.profile.points += score
                        request.user.profile.save()

                        if game == "pyramids":
                            return redirect(pyramids_page)
                        elif game == "serendipity":
                            return redirect(wheel_serendipity_page)
                        elif game == "plush":
                            return redirect(wheel_plush_page)
                else:
                    error = (
                        "You've already sent the maximum scores for this game today."
                    )
                    request.session["error"] = error
                    return redirect(error_page)
        else:
            # AVATARS
            cheat_avatar = Avatar.objects.get(url="pumpkin-eater")
            if cheat_avatar not in request.user.profile.avatars.all():
                request.user.profile.avatars.add(cheat_avatar)
                request.user.profile.save()
                message = Message.objects.create(
                    receiving_user=request.user,
                    subject="You just found a secret avatar!",
                    text='You have just received the avatar "Pumpkin-Eater" to use on the boards!',
                )

            error = "No cheating, please! That ruins the fun for everyone."
            request.session["error"] = error
            return redirect(error_page)
    else:
        error = "You must be logged in to view this page."
        request.session["error"] = error
        return redirect(error_page)
