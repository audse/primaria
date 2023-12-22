from django.shortcuts import render, redirect

from core.models import Pet, Animal, Avatar
from social.models import Message

from utils.error import handle_error, error_page


def create_pet_step_1(request):
    pet = Pet.objects.filter(user=request.user).first()

    if pet is not None:
        handle_error(request, "You can't create another pet when you already have one.")

    animals = Animal.objects.all().order_by("name")
    return render(request, "core/features/create_pet_step_1.html", {"animals": animals})


def create_pet_step_2(request, animal):
    pet = Pet.objects.filter(user=request.user).first()

    if pet is not None:
        handle_error(request, "You can't create another pet when you already have one.")

    animal = Animal.objects.get(name=animal)
    return render(request, "core/features/create_pet_step_2.html", {"animal": animal})


def create_pet_step_3(request, animal):
    pet = Pet.objects.filter(user=request.user).first()

    if pet is not None:
        handle_error(request, "You can't create another pet when you already have one.")

    animal = Animal.objects.get(name=animal)
    color = request.POST.get("color")

    if color in ["red", "yellow", "green", "blue", "black"]:
        error = request.session.pop("error", False)
        if error:
            color = request.session.pop("color", False)
        return render(
            request,
            "core/features/create_pet_step_3.html",
            {"animal": animal, "color": color, "error": error},
        )
    else:
        request.session[
            "error"
        ] = "No cheating, please! That ruins the fun for everyone."
        return redirect(error_page)


def create_pet(request):
    if not request.user.is_authenticated():
        handle_error(request, "You must be logged in to view this page.")

    pet = Pet.objects.filter(user=request.user).first()

    if pet is not None:
        handle_error("You can't create another pet when you already have one.")

    animal = request.POST.get("animal")
    color = request.POST.get("color")
    name = request.POST.get("name")

    check_unique_name = Pet.objects.filter(name=name).first()
    if check_unique_name is not None:
        request.session["error"] = "Sorry, that name is already taken."
        request.session["color"] = color
        return redirect(create_pet_step_3, animal)

    else:
        acceptable_colors = ["red", "yellow", "green", "blue", "black"]
        acceptable_animals = ["dino", "lizard", "monkey", "mouse", "tapir"]
        if color not in acceptable_colors or animal not in acceptable_animals:
            handle_error(
                request, "No cheating, please! That ruins the fun for everyone."
            )

        animal = Animal.objects.get(name=animal)
        all_colors = color + " " + animal.name + ","
        pet = Pet.objects.create(
            user=request.user,
            animal=animal,
            color=color,
            name=name,
            all_colors=all_colors,
        )

        # AVATARS
        pet_avatar = Avatar.objects.get(url=animal.name)
        color_avatar = Avatar.objects.get(url=color)
        request.user.profile.avatars.add(pet_avatar)
        request.user.profile.avatars.add(color_avatar)
        request.user.profile.save()

        message = Message.objects.create(
            receiving_user=request.user,
            subject="You just found some avatars!",
            text="You have just received the avatars %s and %s to use on the boards!"
            % (pet_avatar.name, color_avatar.name),
        )

        return redirect(successful_create_pet_page)


def successful_create_pet_page(request):
    return render(request, "core/features/successful_create_pet_page.html")


def change_pet_page(request):
    if request.user.is_authenticated():
        pet = Pet.objects.filter(user=request.user).first()
        if pet:
            # AVATARS
            red = Avatar.objects.get(url="red")
            yellow = Avatar.objects.get(url="yellow")
            green = Avatar.objects.get(url="green")
            blue = Avatar.objects.get(url="blue")
            black = Avatar.objects.get(url="black")

            dino = Avatar.objects.get(url="dino")
            lizard = Avatar.objects.get(url="lizard")
            monkey = Avatar.objects.get(url="monkey")
            mouse = Avatar.objects.get(url="mouse")
            tapir = Avatar.objects.get(url="tapir")

            color_avatars = [red, yellow, green, blue, black]
            animal_avatars = [dino, lizard, monkey, mouse, tapir]

            for avatar in color_avatars:
                color = avatar.url
                if (
                    "dino " + color in pet.all_colors
                    and "lizard" + color in pet.all_colors
                    and "monkey " + color in pet.all_colors
                    and "mouse " + color in pet.all_colors
                    and "tapir" + color in pet.all_colors
                ):
                    if avatar not in request.user.profile.avatars.all():
                        request.user.profile.avatars.add(avatar)
                        request.user.profile.save()
                        message = Message.objects.create(
                            receiving_user=request.user,
                            subject="You just found a secret avatar!",
                            text='You have just received the avatar "'
                            + avatar.name
                            + '" to use on the boards!',
                        )

            for avatar in animal_avatars:
                animal = avatar.url
                if (
                    animal + " red" in pet.all_colors
                    and animal + " yellow" in pet.all_colors
                    and animal + " green" in pet.all_colors
                    and animal + " blue" in pet.all_colors
                    and animal + " black" in pet.all_colors
                ):
                    if avatar not in request.user.profile.avatars.all():
                        request.user.profile.avatars.add(avatar)
                        request.user.profile.save()
                        message = Message.objects.create(
                            receiving_user=request.user,
                            subject="You just found a secret avatar!",
                            text='You have just received the avatar "'
                            + avatar.name
                            + '" to use on the boards!',
                        )

            rainbow_avatar = Avatar.objects.get(url="rainbow")
            if rainbow_avatar not in request.user.profile.avatars.all():
                if (
                    "red" in pet.all_colors
                    and "yellow" in pet.all_colors
                    and "green" in pet.all_colors
                    and "blue" in pet.all_colors
                    and "black" in pet.all_colors
                ):
                    all_colors_count = len(pet.all_colors.split(",").pop())
                    if all_colors_count >= 10:
                        request.user.profile.avatars.add(rainbow_avatar)
                        request.user.profile.save()
                        message = Message.objects.create(
                            receiving_user=request.user,
                            subject="You just found a secret avatar!",
                            text='You have just received the avatar "'
                            + rainbow_avatar.name
                            + '" to use on the boards!',
                        )

            all_colors = pet.all_colors.split(",")
            for n in range(0, len(all_colors) - 1):
                all_colors[n] = all_colors[n].split(" ")
                n += 1
            all_colors = tuple(all_colors)

            return render(
                request, "core/change_pet_page.html", {"all_colors": all_colors}
            )
        else:
            request.session["error"] = "You must have a pet to view this page."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def change_pet(request):
    current_pet = Pet.objects.filter(user=request.user).first()

    requested_color = request.POST.get("color")
    requested_animal_name = request.POST.get("animal")

    requested_string = "%s %s," % (requested_color, requested_animal_name)
    requested_animal = Animal.objects.filter(name=requested_animal_name).first()

    if not request.user.is_authenticated():
        return handle_error(request, "You must be logged in to view this page.")
    if not current_pet:
        return handle_error(request, "You must have a pet to view this page.")
    if requested_string not in current_pet.all_colors:
        return handle_error(
            request, "You cannot make a pet a color you haven't unlocked."
        )
    if not requested_animal:
        return handle_error(request, "That animal does not exist.")

    current_pet.color = requested_color
    current_pet.animal = requested_animal
    current_pet.save()

    return redirect(change_pet_page)
