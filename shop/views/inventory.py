from django.shortcuts import render, redirect
from ..models import Category, Inventory
from core.models import Animal, Pet
import random
from utils import avatars
from utils.error import error_page


def inventory_page(request):
    if request.user.is_authenticated:
        items = Inventory.objects.filter(user=request.user, box=False, pending=False)
        item_count = items.count()

        # AVATARS
        avatars.get_feeling_blue(request, inventory_items=items)

        results = request.session.pop("results", False)
        return render(
            request,
            "shop/inventory_page.html",
            {"items": items, "item_count": item_count, "results": results},
        )
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def use_item(request):
    if request.user.is_authenticated:
        inventory_pk = request.POST.get("inventory_pk")
        inventory = Inventory.objects.filter(
            user=request.user, box=False, pending=False, pk=inventory_pk
        ).first()
        if inventory != None and inventory.item.usable:
            pet = Pet.objects.filter(user=request.user).first()
            if pet:
                potion_category = Category.objects.filter(name="potion").first()
                if inventory.item.category != potion_category:
                    if inventory.item.hunger != 10:  # 50% chance of working
                        if (pet.hunger + inventory.item.hunger) <= 0:
                            pet.hunger = 1
                        elif (pet.hunger + inventory.item.hunger) <= 5:
                            pet.hunger += inventory.item.hunger
                        else:
                            pet.hunger = 5
                    else:
                        chance = random.randint(1, 2)
                        if chance == 1:
                            if (pet.hunger + 1) <= 0:
                                pet.hunger = 1
                            elif (pet.hunger + 1) <= 5:
                                pet.hunger += 1
                            else:
                                pet.hunger = 5

                    if inventory.item.wellness != 10:  # 50% chance of working
                        if (pet.wellness + inventory.item.wellness) <= 0:
                            pet.wellness = 1
                        elif (pet.wellness + inventory.item.wellness) <= 5:
                            pet.wellness += inventory.item.wellness
                        else:
                            pet.wellness = 5
                    else:
                        chance = random.randint(1, 2)
                        if chance == 1:
                            if (pet.wellness + 1) <= 0:
                                pet.wellness = 1
                            elif (pet.wellness + 1) <= 5:
                                pet.wellness += 1
                            else:
                                pet.wellness = 5

                    if inventory.item.happiness != 10:  # 50% chance of working
                        if (pet.happiness + inventory.item.happiness) <= 0:
                            pet.happiness = 1
                        elif (pet.happiness + inventory.item.happiness) <= 5:
                            pet.happiness += inventory.item.happiness
                        else:
                            pet.happiness = 5
                    else:
                        chance = random.randint(1, 2)
                        if chance == 1:
                            if (pet.happiness + 1) <= 0:
                                pet.happiness = 1
                            elif (pet.happiness + 1) <= 5:
                                pet.happiness += 1
                            else:
                                pet.happiness = 5

                    pet.save()

                    # AVATARS
                    avatars.get_sweet(request, pet, inventory_item=inventory)

                    inventory.delete()
                    request.session["results"] = (
                        "You have used your " + inventory.item.name + "!"
                    )
                    return redirect(inventory_page)

                else:  # item is a potion
                    color_potion_category = Category.objects.filter(
                        name="color potion"
                    ).first()
                    morph_potion_category = Category.objects.filter(
                        name="morph potion"
                    ).first()
                    colormorph_potion_category = Category.objects.filter(
                        name="colormorph potion"
                    ).first()
                    mystery_potion_category = Category.objects.filter(
                        name="mystery potion"
                    ).first()
                    stat_potion_category = Category.objects.filter(
                        name="stat potion"
                    ).first()
                    if inventory.item.second_category == color_potion_category:
                        old_color = pet.color
                        new_color = inventory.item.url.replace("-potion", "")
                        pet.color = new_color
                        pet.all_colors += new_color + " " + pet.animal.name + ","
                        pet.save()
                        inventory.delete()
                        request.session["results"] = (
                            "Your "
                            + old_color
                            + " "
                            + pet.animal.name
                            + " has transformed into a "
                            + new_color
                            + " "
                            + pet.animal.name
                            + "!"
                        )

                        # AVATARS
                        avatars.get_starry_night(request, pet)

                        return redirect(potion_results_page)

                    elif inventory.item.second_category == morph_potion_category:
                        old_species = pet.animal.name
                        new_species = Animal.objects.filter(
                            name=inventory.item.url.replace("-potion", "")
                        ).first()
                        pet.animal = new_species
                        pet.all_colors += pet.color + " " + new_species.name + ","
                        pet.save()
                        inventory.delete()
                        request.session["results"] = (
                            "Your "
                            + old_species
                            + " has transformed into a "
                            + new_species.name
                            + "!"
                        )

                        # AVATARS
                        avatars.get_witch(request)

                        return redirect(potion_results_page)
                    elif inventory.item.second_category == colormorph_potion_category:
                        old_species = pet.animal.name
                        old_color = pet.color

                        new = inventory.item.url.split(
                            "-"
                        )  # returns color, animal, potion
                        if "knit" in new:
                            new = ["%s-knit" % (new[0]), new[2], new[3]]
                        new.pop()  # remove -potion
                        new_species = Animal.objects.get(name=new[1])
                        new_color = new[0]

                        pet.animal = new_species
                        pet.color = new_color
                        add_color = new_color + " " + new_species.name + ","
                        pet.all_colors += add_color
                        pet.save()
                        inventory.delete()

                        request.session["results"] = (
                            "Your "
                            + old_color
                            + " "
                            + old_species
                            + " has transformed into a "
                            + new_color
                            + " "
                            + new_species.name
                            + "!"
                        )
                        return redirect(potion_results_page)

                    elif inventory.item.second_category == stat_potion_category:
                        if inventory.item.url.replace("-potion", "") == "hunger":
                            pet.hunger = 5
                            pet.save()
                            inventory.delete()
                            request.session[
                                "results"
                            ] = "Your pet's hunger is now at maximum!"

                            # Avatars
                            avatars.get_that_tasted_funny(request)

                            return redirect(potion_results_page)

                        elif inventory.item.url.replace("-potion", "") == "happiness":
                            pet.happiness = 5
                            pet.save()
                            inventory.delete()
                            request.session[
                                "results"
                            ] = "Your pet's happiness is now at maximum!"
                            return redirect(potion_results_page)

                        elif inventory.item.url.replace("-potion", "") == "wellness":
                            pet.wellness = 5
                            pet.save()
                            inventory.delete()
                            request.session[
                                "results"
                            ] = "Your pet's wellness is now at maximum!"
                            return redirect(potion_results_page)

                    elif inventory.item.second_category == mystery_potion_category:
                        stat = random.randint(1, 4)
                        change = random.randint(-2, 2)

                        request.session["results"] = "Your pet feels a bit funny..."

                        if stat == 1:
                            pet.hunger += change
                            if pet.hunger <= 1:
                                pet.hunger == 1
                            elif pet.hunger >= 5:
                                pet.hunger == 5
                            pet.save()
                            request.session[
                                "results"
                            ] += " Its' hunger changes by a bit."
                        elif stat == 2:
                            pet.wellness += change
                            if pet.wellness <= 1:
                                pet.wellness == 1
                            elif pet.wellness >= 5:
                                pet.wellness == 5
                            pet.save()
                            request.session[
                                "results"
                            ] += " Its' wellness changes by a bit."
                        elif stat == 3:
                            pet.happiness += change
                            if pet.happiness <= 1:
                                pet.happiness == 1
                            elif pet.happiness >= 5:
                                pet.happiness == 5
                            pet.save()
                            request.session[
                                "results"
                            ] += " Its' happiness changes by a bit."
                        elif stat == 4:
                            change_1 = random.randint(-1, 1)
                            change_2 = random.randint(-1, 1)
                            change_3 = random.randint(-1, 1)
                            pet.hunger += change_1
                            if pet.hunger <= 1:
                                pet.hunger == 1
                            elif pet.hunger >= 5:
                                pet.hunger == 5
                            pet.wellness += change_2
                            if pet.wellness <= 1:
                                pet.wellness == 1
                            elif pet.wellness >= 5:
                                pet.wellness == 5
                            pet.happiness += change_3
                            if pet.happiness <= 1:
                                pet.happiness == 1
                            elif pet.happiness >= 5:
                                pet.happiness == 5
                            pet.save()
                            request.session[
                                "results"
                            ] += " All of its' stats change a bit."
                        inventory.delete()
                        return redirect(potion_results_page)

                    else:
                        request.session["error"] = "Sorry, that potion was not found."
                        return redirect(error_page)
            else:
                request.session["error"] = "You must have a pet to use an item."
                return redirect(error_page)
        else:
            request.session["error"] = "You cannot use that item at this time."
            return redirect(error_page)
    else:
        request.session["error"] = "You must be logged in to view this page."
        return redirect(error_page)


def potion_results_page(request):
    results = request.session.pop("results", False)
    if results == False:
        results = "We are not sure what went wrong, but we will work on fixing it."
    pet = Pet.objects.filter(user=request.user).first()
    if pet is None:
        request.session["error"] = "You must have a pet to view this page."
        return redirect(error_page)
    return render(
        request, "shop/potion_results_page.html", {"results": results, "pet": pet}
    )
