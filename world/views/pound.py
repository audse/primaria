from django.shortcuts import render, redirect
from core.models import Pet
from utils.error import error_page
from core.views.pets import successful_create_pet_page


def pound_page(request):
    pound_pets = Pet.objects.filter(user=None).order_by("?")[:3]
    try:
        pet = Pet.objects.get(user=request.user)
    except:
        pet = None
    return render(
        request, "world/pound_page.html", {"pound_pets": pound_pets, "pet": pet}
    )


def adopt_from_pound(request, adopt):
    if request.user.is_authenticated:
        try:
            pet = Pet.objects.get(user=request.user)
        except:
            pet = None
        if pet == None:
            try:
                adopt = Pet.objects.get(name=adopt, user=None)
            except:
                adopt = None

            if adopt != None:
                adopt.user = request.user
                adopt.save()
                return redirect(successful_create_pet_page)
            else:
                request.session["error"] = "No adoptable pet with that name was found."
                return redirect(error_page)
        else:
            request.session[
                "error"
            ] = "You cannot adopt a pet when you already have one."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def give_up_pet(request):
    if request.user.is_authenticated:
        pet = Pet.objects.get(user=request.user).first()
        if pet:
            pet.user = None
            pet.all_colors = pet.color + " " + pet.animal.name
            pet.save()
            return redirect(pound_page)
        else:
            request.session["error"] = "You do not have a pet to give up."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)
