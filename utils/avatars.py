
import random
from datetime import datetime
from core.models import Pet, Avatar
from social.models import Message

def send_avatar_message (request, avatar_name):
    Message.objects.create(
            receiving_user=request.user,
            subject="You just found a secret avatar!",
            text="You have just received the avatar \"%s\" to use on the boards!"%(avatar_name)
        )

# Get the "Feeling Blue" avatar when you have a blue pet and 5 or more blue items in your inventory
def get_feeling_blue (request, inventory_items):
    feeling_blue_avatar = Avatar.objects.get(url="feeling-blue")
    if feeling_blue_avatar not in request.user.profile.avatars.all():
        pet = Pet.objects.filter(user=request.user).first()
        if pet is not None and "blue" in pet.color:
            blue_items = 0
            for item in inventory_items:
                if "blue" in item.item.name.lower():
                    blue_items += 1
            if blue_items >= 5:
                request.user.profile.avatars.add(feeling_blue_avatar)
                request.user.profile.save()
                send_avatar_message(request, 'Feeling Blue')

# Get the "Sweet~" avatar when you have a sprinkle pet and you feed it a cupcake
def get_sweet (request, pet, inventory_item):
    sweet_avatar = Avatar.objects.get(url="sweet")
    if sweet_avatar not in request.user.profile.avatars.all():
        if pet.color == "sprinkle" and "cupcake" in inventory_item.item.name.lower():
            request.user.profile.avatars.add(sweet_avatar)
            request.user.profile.save()
            send_avatar_message(request, 'Sweet~')

# Get the "Starry Night" avatar when you use a starry potion at night
def get_starry_night (request, pet):
    starry_night_avatar = Avatar.objects.get(url="starry-night")
    if starry_night_avatar not in request.user.profile.avatars.all():
        if pet.color == "starry":
            today = datetime.today()
            if today.hour > 18 and today.hour < 24 or today.hour > 0 and today.hour < 6:
                request.user.profile.avatars.add(starry_night_avatar)
                request.user.profile.save()
                send_avatar_message(request, 'Starry Night')

# Get the "Witch!!!" avatar at random when you use a morph potion
def get_witch (request):
    rand_num = random.randint(1, 4)
    if rand_num == 1:
        witch_avatar = Avatar.objects.get(url="witch")
        if witch_avatar not in request.user.profile.avatars.all():
            request.user.profile.avatars.add(witch_avatar)
            request.user.profile.save()
            send_avatar_message(request, "Witch!!!")

# Get the "That Tasted Funny..." avatar at random when feeding your pet a hunger stat potion
def get_that_tasted_funny (request):
    rand_num = random.randint(1, 4)
    if rand_num == 1:
        funny_avatar = Avatar.objects.get(url="that-tasted-funny")
        if funny_avatar not in request.user.profile.avatars.all():
            request.user.profile.avatars.add(funny_avatar)
            request.user.profile.save()
            send_avatar_message(request, 'That Tasted Funny...')

# Get the "Yay! Pink!!" avatar when purchasing a pink item
def get_yay_pink (request, inventory_item):
    pet = Pet.objects.filter(user=request.user).first()
    if pet is not None:
        pink_avatar = Avatar.objects.get(url="yay-pink")
        if pink_avatar not in request.user.profile.avatars.all():
            if "pink" in inventory_item.item.name.lower():
                request.user.profile.avatars.add(pink_avatar)
                request.user.profile.save()
                send_avatar_message(request, 'Yay! Pink!!')