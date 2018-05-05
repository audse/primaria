from django.template import Library
from datetime import datetime
from datetime import timedelta

from core.models import Profile

register = Library()

@register.filter(name="get_users_online")
def get_users_online(var):
	today = datetime.today()
	today = today - timedelta(hours=1)
	# users_online = Profile.objects.filter(last_online__year=today.year, last_online__month=today.month, last_online__day=today.day, last_online__hour__gte=today.hour).count()
	users_online = Profile.objects.filter(last_online__gte=today).order_by('-last_online').count()
	return users_online