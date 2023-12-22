from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.core.paginator import Paginator


from ..models import Category, Item, Inventory, Gallery
from social.models import Message, Badge
from core.models import Pet, Avatar

from utils.error import handle_error, require_login, error_page


def gallery_page(request):
    if request.user.is_authenticated():
        gallery = Gallery.objects.filter(user=request.user).first()
        if gallery:
            plush_category = Category.objects.get(name="plush")
            card_category = Category.objects.get(name="playing card")

            total_available_plush = Item.objects.filter(category=plush_category).count()
            total_available_cards = Item.objects.filter(category=card_category).count()
            inventory_plush = Inventory.objects.filter(
                user=request.user,
                item__category=plush_category,
                box=False,
                pending=False,
            )
            inventory_cards = Inventory.objects.filter(
                user=request.user,
                item__category=card_category,
                box=False,
                pending=False,
            )
            gallery_plush = gallery.plush.all().order_by("name")
            gallery_cards = gallery.cards.all().order_by("name")
            total_items_in_gallery = gallery_plush.count() + gallery_cards.count()

            return render(
                request,
                "shop/gallery_page.html",
                {
                    "gallery": gallery,
                    "total_plush": total_available_plush,
                    "total_cards": total_available_cards,
                    "user_plush": inventory_plush,
                    "user_cards": inventory_cards,
                    "gallery_plush": gallery_plush,
                    "gallery_cards": gallery_cards,
                    "total_items_in_gallery": total_items_in_gallery,
                },
            )
        else:
            return render(request, "shop/gallery_page.html", {"gallery": gallery})
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def user_gallery_page(request, username):
    user = User.objects.filter(username=username).first()
    if user:
        gallery = Gallery.objects.filter(user=user).first()
        if gallery:
            plush_category = Category.objects.get(name="plush")
            card_category = Category.objects.get(name="playing card")
            total_available_plush = Item.objects.filter(category=plush_category).count()
            total_available_cards = Item.objects.filter(category=card_category).count()
            gallery_plush = gallery.plush.all().order_by("name")
            gallery_cards = gallery.cards.all().order_by("name")
            return render(
                request,
                "shop/user_gallery_page.html",
                {
                    "gallery": gallery,
                    "total_plush": total_available_plush,
                    "gallery_plush": gallery_plush,
                    "total_cards": total_available_cards,
                    "gallery_cards": gallery_cards,
                },
            )
        else:
            request.session["error"] = "That user does not yet have a gallery."
            return redirect(error_page)
    else:
        request.session["error"] = "No user with that username exists."
        return redirect(error_page)


def open_gallery_page(request):
    if request.user.is_authenticated():
        gallery = Gallery.objects.filter(user=request.user).first()
        if gallery is None:
            return render(request, "shop/open_gallery_page.html")
        else:
            request.session["error"] = "You have already created a gallery."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def open_gallery(request):
    if request.user.is_authenticated():
        gallery = Gallery.objects.filter(user=request.user).first()
        if gallery is None:
            if request.user.profile.points >= 500:
                request.user.profile.points -= 500
                request.user.profile.save()
                gallery = Gallery.objects.create(
                    user=request.user, name=request.POST.get("gallery_name")
                )
                return redirect(gallery_page)
            else:
                request.session[
                    "error"
                ] = "You do not have enough points to open a gallery."
                return redirect(error_page)
        else:
            request.session["error"] = "You have already created a gallery."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def add_gallery_item(request):
    if request.user.is_authenticated():
        gallery = Gallery.objects.filter(user=request.user).first()
        if gallery:
            item = request.POST.get("item")
            try:
                item = int(item)
            except:
                request.session["error"] = "That item does not exist."
                return redirect(error_page)

            item = Inventory.objects.filter(
                user=request.user, pk=item, box=False, pending=False
            ).first()
            if item:
                if (gallery.plush.count() + gallery.cards.count()) < gallery.space:
                    if item.item.category.name == "plush":
                        if item.item not in gallery.plush.all():
                            if gallery.plush.count() == 9:  # will now become 10
                                subject = "Congratulations!"
                                text = "You have just reached 10 plushies in your gallery! You have been awarded the Amateur Plushie Collector Badge."
                                message = Message.objects.create(
                                    receiving_user=request.user,
                                    subject=subject,
                                    text=text,
                                )
                                badge = Badge.objects.create(
                                    user=request.user,
                                    rank="amateur",
                                    area="plush-collecting",
                                )
                            elif gallery.plush.count() == 49:  # will now become 50
                                subject = "Congratulations!"
                                text = "You have just reached 10 plushies in your gallery! You have been awarded the Professional Plushie Collector Badge."
                                message = Message.objects.create(
                                    receiving_user=request.user,
                                    subject=subject,
                                    text=text,
                                )
                                badge = Badge.objects.create(
                                    user=request.user,
                                    rank="professional",
                                    area="plush-collecting",
                                )

                            gallery.plush.add(item.item)
                            gallery.save()
                            item.delete()

                            # AVATARS
                            historic_avatar = Avatar.objects.get(url="historic")
                            if (
                                historic_avatar
                                not in request.user.profile.avatars.all()
                            ):
                                pet = Pet.objects.filter(user=request.user).first()
                                if pet is not None:
                                    if pet.color == "baroque":
                                        request.user.profile.avatars.add(
                                            historic_avatar
                                        )
                                        request.user.profile.save()
                                        message = Message.objects.create(
                                            receiving_user=request.user,
                                            subject="You just found a secret avatar!",
                                            text='You have just received the avatar "Historic" to use on the boards!',
                                        )

                            return redirect(gallery_page)
                        else:
                            request.session[
                                "error"
                            ] = "That item is already in your gallery."
                            return redirect(error_page)
                    elif item.item.category.name == "playing card":
                        if item.item not in gallery.cards.all():
                            if gallery.cards.count() == 9:  # will now become 10
                                subject = "Congratulations!"
                                text = "You have just reached 10 cards in your gallery! You have been awarded the Amateur Card Collector Badge."
                                message = Message.objects.create(
                                    receiving_user=request.user,
                                    subject=subject,
                                    text=text,
                                )
                                badge = Badge.objects.create(
                                    user=request.user,
                                    rank="amateur",
                                    area="card-collecting",
                                )
                            elif gallery.cards.count() == 49:  # will now become 50
                                subject = "Congratulations!"
                                text = "You have just reached 10 cards in your gallery! You have been awarded the Professional Card Collector Badge."
                                message = Message.objects.create(
                                    receiving_user=request.user,
                                    subject=subject,
                                    text=text,
                                )
                                badge = Badge.objects.create(
                                    user=request.user,
                                    rank="professional",
                                    area="card-collecting",
                                )

                            gallery.cards.add(item.item)
                            gallery.save()
                            item.delete()

                            # AVATARS
                            pet = Pet.objects.filter(user=request.user).first()
                            if pet is not None:
                                if pet.color == "baroque":
                                    historic_avatar = Avatar.objects.get(url="historic")
                                    request.user.profile.avatars.add(historic_avatar)
                                    request.user.profile.save()
                                    message = Message.objects.create(
                                        receiving_user=request.user,
                                        subject="You just found a secret avatar!",
                                        text='You have just received the avatar "Historic" to use on the boards!',
                                    )

                            return redirect(gallery_page)
                        else:
                            request.session[
                                "error"
                            ] = "That item is already in your gallery."
                            return redirect(error_page)
                else:
                    request.session["error"] = "Your gallery is full right now."
                    return redirect(error_page)
            else:
                request.session["error"] = "That item does not exist."
                return redirect(error_page)
        else:
            request.session["error"] = "You have not yet created a gallery."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def upgrade_gallery(request):
    if request.user.is_authenticated():
        gallery = Gallery.objects.filter(user=request.user).first()
        if gallery:
            if request.user.profile.points >= gallery.upgrade_cost:
                request.user.profile.points -= gallery.upgrade_cost
                request.user.profile.save()

                gallery.space += 5
                gallery.upgrade_cost = 100 * gallery.space
                gallery.save()
                return redirect(gallery_page)
            else:
                request.session[
                    "error"
                ] = "You do not have enough points to upgrade your gallery."
                return redirect(error_page)
        else:
            request.session["error"] = "You have not yet created a gallery."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def rename_gallery(request):
    if request.user.is_authenticated():
        gallery = Gallery.objects.filter(user=request.user).first()
        if gallery:
            new_gallery_name = request.POST.get("new_gallery_name")
            gallery.name = new_gallery_name
            gallery.save()
            return redirect(gallery_page)
        else:
            request.session["error"] = "You have not yet created a gallery."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)
