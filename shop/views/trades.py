from django.shortcuts import render, redirect

from django.core.paginator import Paginator

from ..models import Category, Inventory, Trade
from social.models import Message
from core.models import Avatar

from utils.error import handle_error, require_login, error_page


def trading_post_page(request):
    if request.user.is_authenticated():
        all_open_trades = Trade.objects.filter(original_trade=None).order_by("-date")
        paginator = Paginator(all_open_trades, 10)
        page = request.GET.get("page")
        if page:
            try:
                page = int(page)
            except:
                request.session["error"] = "Page must be an integer."
                return redirect(error_page)
            all_trades = paginator.page(page)
        else:
            all_trades = paginator.page(1)

        return render(
            request, "shop/trading_post_page.html", {"all_trades": all_trades}
        )
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def open_trade_page(request):
    if request.user.is_authenticated():
        inventory = Inventory.objects.filter(
            user=request.user, box=False, pending=False
        )
        return render(request, "shop/open_trade_page.html", {"inventory": inventory})
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def open_trade(request):
    if request.user.is_authenticated():
        items = request.POST.get("items")
        message = request.POST.get("message")
        if items:
            items = items.split(",")
            items_to_trade = []
            for item in items:
                item = int(item)
                item = Inventory.objects.filter(
                    user=request.user, box=False, pending=False, pk=item
                ).first()
                if item is None:
                    request.session["error"] = "All items must be your own."
                    return redirect(error_page)
                items_to_trade.append(item)
            if len(items_to_trade) <= 5:
                trade = Trade.objects.create(sending_user=request.user, message=message)
                trade.save()
                for item in items_to_trade:
                    item.pending = True
                    item.save()
                    trade.items.add(item)
                    trade.save()

                return redirect(trading_post_page)
            else:
                request.session[
                    "error"
                ] = "You may only trade up to five items at a time."
                return redirect(error_page)
        else:
            request.session["error"] = "You must select at least one item."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def your_trades_page(request):
    if request.user.is_authenticated():
        your_trades = Trade.objects.filter(
            sending_user=request.user, original_trade=None
        ).order_by("-date")
        your_offers = (
            Trade.objects.filter(sending_user=request.user)
            .exclude(original_trade=None)
            .order_by("-date")
        )

        for trade in your_trades:
            trade.offers = Trade.objects.filter(original_trade=trade).order_by("-date")
        return render(
            request,
            "shop/your_trades_page.html",
            {"your_trades": your_trades, "your_offers": your_offers},
        )
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def make_offer_page(request, pk):
    if request.user.is_authenticated():
        original = Trade.objects.filter(pk=pk).first()
        if original:
            inventory = Inventory.objects.filter(
                user=request.user, box=False, pending=False
            )
            return render(
                request,
                "shop/make_offer_page.html",
                {"original": original, "inventory": inventory},
            )
        else:
            request.session["error"] = "That trade was not found."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def make_offer(request):
    if request.user.is_authenticated():
        original = int(request.POST.get("original"))
        original = Trade.objects.filter(pk=original).first()
        if original:
            items = request.POST.get("items")
            message = request.POST.get("message")
            if items:
                items = items.split(",")
                items_to_trade = []
                for item in items:
                    item = int(item)
                    item = Inventory.objects.filter(
                        user=request.user, box=False, pending=False, pk=item
                    ).first()
                    if item is None:
                        request.session["error"] = "All items must be your own."
                        return redirect(error_page)
                    items_to_trade.append(item)
                if len(items_to_trade) <= 5:
                    trade = Trade.objects.create(
                        original_trade=original,
                        sending_user=request.user,
                        message=message,
                    )
                    trade.save()
                    for item in items_to_trade:
                        item.pending = True
                        item.save()
                        trade.items.add(item)
                        trade.save()

                    message = Message.objects.create(
                        receiving_user=original.sending_user,
                        subject="You have received an offer on your trade!",
                        text=request.user.username
                        + " has sent an offer on your trade. Check your trades and offers page to see it.",
                    )
                    return redirect(your_trades_page)

                else:
                    request.session[
                        "error"
                    ] = "You may only trade up to five items at a time."
                    return redirect(error_page)
            else:
                request.session["error"] = "You must select at least one item."
                return redirect(error_page)
        else:
            request.session["error"] = "That trade was not found."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def accept_offer(request, original_pk, offer_pk):
    if request.user.is_authenticated():
        original_trade = Trade.objects.filter(
            sending_user=request.user, pk=original_pk
        ).first()
        offer = Trade.objects.filter(pk=offer_pk, original_trade=original_trade).first()
        if original_trade and offer:
            for item in original_trade.items.all():
                item.user = offer.sending_user
                item.pending = False
                item.save()
            for item in offer.items.all():
                item.user = original_trade.sending_user
                item.pending = False
                item.save()
            message = Message.objects.create(
                receiving_user=original_trade.sending_user,
                subject="The trade has been completed!",
                text="The items can be found in your inventory. Note that if you now have over fifty items, you will not be able to get any more unless you remove some first.",
            )
            message = Message.objects.create(
                receiving_user=offer.sending_user,
                subject="Your offer has been accepted!",
                text="The items can be found in your inventory. Note that if you now have over fifty items, you will not be able to get any more unless you remove some first.",
            )

            rejected_offers = Trade.objects.filter(
                original_trade=original_trade
            ).exclude(pk=offer_pk)
            for offer in rejected_offers:
                message = Message.objects.create(
                    receiving_user=offer.sending_user,
                    subject="Your offer has been rejected.",
                    text="Sorry, but your offer has been rejected. The items have been put back in your inventory. Note that if you now have over fifty items, you will not be able to get any more unless you remove some first.",
                )
                for item in offer.items.all():
                    item.pending = False
                    item.save()
                offer.delete()

            # AVATARS
            trading_cards_avatar = Avatar.objects.get(url="trading-cards")
            if trading_cards_avatar not in request.user.profile.avatars.all():
                can_get_av = True
                for item in original_trade.items.all():
                    if item.item.category != Category.objects.get(name="playing card"):
                        can_get_av = False
                        break
                for item in offer.items.all():
                    if item.item.category != Category.objects.get(name="playing card"):
                        can_get_av = False
                        break
                if can_get_av:
                    request.user.profile.avatars.add(trading_cards_avatar)
                    request.user.profile.save()
                    message = Message.objects.create(
                        receiving_user=request.user,
                        subject="You just found a secret avatar!",
                        text='You have just received the avatar "Trading Cards" to use on the boards!',
                    )

                    if (
                        trading_cards_avatar
                        not in offer.sending_user.profile.avatars.all()
                    ):
                        offer.sending_user.profile.avatars.add(trading_cards_avatar)
                        offer.sending_user.profile.save()
                        message = Message.objects.create(
                            receiving_user=offer.sending_user,
                            subject="You just found a secret avatar!",
                            text='You have just received the avatar "Trading Cards" to use on the boards!',
                        )

            original_trade.delete()
            offer.delete()
            return redirect(your_trades_page)
        else:
            request.session["error"] = "Those trades were not found."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def cancel_trade(request, trade_pk):
    if request.user.is_authenticated():
        trade = Trade.objects.filter(
            sending_user=request.user, pk=trade_pk, original_trade=None
        ).first()
        if trade:
            message = Message.objects.create(
                receiving_user=trade.sending_user,
                subject="Your trade has been cancelled.",
                text="The items have been put back in your inventory. Note that if you now have over fifty items, you will not be able to get any more unless you remove some first.",
            )
            for item in trade.items.all():
                item.pending = False
                item.save()

            rejected_offers = Trade.objects.filter(original_trade=trade)
            for offer in rejected_offers:
                message = Message.objects.create(
                    receiving_user=offer.sending_user,
                    subject="Your offer has been rejected.",
                    text="Sorry, but your offer has been rejected. The items have been put back in your inventory. Note that if you now have over fifty items, you will not be able to get any more unless you remove some first.",
                )
                for item in offer.items.all():
                    item.pending = False
                    item.save()
                offer.delete()
            trade.delete()

            return redirect(your_trades_page)
        else:
            request.session["error"] = "Those trades were not found."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)
