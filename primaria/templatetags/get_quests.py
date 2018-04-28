from django.template import Library

from goddess.models import Quest
from datetime import datetime

register = Library()

@register.filter()
def get_quests(user, goddess):
	today = datetime.today()
	quests_today = Quest.objects.filter(user=user, goddess=goddess, completed=True, date__year=today.year, date__month=today.month, date__day=today.day).count()
	return quests_today