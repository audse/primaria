from django.shortcuts import render, redirect

from datetime import datetime
import random

from ..models import MedicinePickup
from shop.models import Item, Category, Inventory
from core.models import Pet
from utils.error import error_page


def hospital_page(request):
    if request.user.is_authenticated():
        pet = Pet.objects.filter(user=request.user).first()
        medicine = MedicinePickup.objects.filter(user=request.user).first()
    else:
        pet = None
        medicine = None
    return render(
        request, "world/hospital_page.html", {"pet": pet, "medicine": medicine}
    )


def make_hospital_appointment(request):
    if request.user.is_authenticated():
        pet = Pet.objects.filter(user=request.user).first()
        if pet:
            if pet.wellness < 3:
                medicine = MedicinePickup.objects.filter(user=request.user).first()
                if medicine is None:
                    if request.user.profile.points >= 500:
                        request.user.profile.points -= 500
                        request.user.profile.save()
                        category = Category.objects.filter(name="medicine").first()
                        medicine = (
                            Item.objects.filter(category=category).order_by("?").first()
                        )
                        medicine_pickup = MedicinePickup.objects.create(
                            user=request.user, item=medicine
                        )
                        return redirect(hospital_page)
                    else:
                        request.session[
                            "error"
                        ] = "You do not have enough points to make a hospital appointment."
                        return redirect(error_page)
                else:
                    request.session[
                        "error"
                    ] = "You cannot make hospital appointment when you already have medicine to pick up."
                    return redirect(error_page)
            else:
                request.session[
                    "error"
                ] = "Your pet is not sick enough to make a hospital appointment."
                return redirect(error_page)
        else:
            request.session["error"] = "You must have a pet to view this page."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def pickup_hospital_medicine(request):
    if request.user.is_authenticated():
        pet = Pet.objects.filter(user=request.user).first()
        if pet:
            medicine = MedicinePickup.objects.filter(user=request.user).first()
            if medicine is not None:
                if request.user.profile.points >= 250:
                    if (
                        Inventory.objects.filter(
                            user=request.user, box=False, pending=False
                        ).count()
                        < 50
                    ):
                        request.user.profile.points -= 250
                        request.user.profile.save()
                        inventory = Inventory.objects.create(
                            user=request.user, item=medicine.item
                        )
                        medicine.delete()
                        return redirect(hospital_page)
                    else:
                        request.session[
                            "error"
                        ] = "You can only have up to 50 items in your inventory."
                        return redirect(error_page)
                else:
                    request.session[
                        "error"
                    ] = "You do not have enough points to pick up your medicine."
                    return redirect(error_page)
            else:
                request.session["error"] = "You do not have any medicine to pick up."
                return redirect(error_page)
        else:
            request.session["error"] = "You must have a pet to view this page."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)
