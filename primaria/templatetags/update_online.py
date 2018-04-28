from django.template import Library
from django.utils import timezone

register = Library()

@register.filter(name="update_online")
def update_online(user):
	user.profile.last_online = timezone.now()
	user.profile.save()
	return "Updating online users page..."