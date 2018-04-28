from django.template import Library
from world.models import DailyClaim
from datetime import datetime, timedelta

register = Library()

@register.filter(name="login_bonus")
def login_bonus(user):
	today = datetime.today()
	claim = DailyClaim.objects.filter(user=user, daily_type="login", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
	if claim is None:
		one_day_ago = today - timedelta(days=1)
		two_days_ago = today - timedelta(days=2)
		three_days_ago = today - timedelta(days=3)
		four_days_ago = today - timedelta(days=4)

		one_day_ago_claim = DailyClaim.objects.filter(user=user, daily_type="login", date_of_claim__year=one_day_ago.year, date_of_claim__month=one_day_ago.month, date_of_claim__day=one_day_ago.day).first()
		two_days_ago_claim = DailyClaim.objects.filter(user=user, daily_type="login", date_of_claim__year=two_days_ago.year, date_of_claim__month=two_days_ago.month, date_of_claim__day=two_days_ago.day).first()
		three_days_ago_claim = DailyClaim.objects.filter(user=user, daily_type="login", date_of_claim__year=three_days_ago.year, date_of_claim__month=three_days_ago.month, date_of_claim__day=three_days_ago.day).first()
		four_days_ago_claim = DailyClaim.objects.filter(user=user, daily_type="login", date_of_claim__year=four_days_ago.year, date_of_claim__month=four_days_ago.month, date_of_claim__day=four_days_ago.day).first()

		login_bonus = 1
		if one_day_ago_claim != None:
			login_bonus = 2
			if two_days_ago_claim != None:
				login_bonus = 3
				if three_days_ago_claim != None:
					login_bonus = 4
					if four_days_ago_claim != None:
						login_bonus = 5
						
		return login_bonus
	else:
		return None