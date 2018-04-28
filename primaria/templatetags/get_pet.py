from django.template import Library
from core.models import Pet

register = Library()

@register.filter(name="get_pet")
def get_pet(user):
    pet = Pet.objects.filter(user=user).first()
    if pet is not None:
        return pet
    else:
        return None
