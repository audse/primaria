import datetime
import celery
from celery.task.schedules import crontab

from django.contrib.auth.models import User
from social.models import Message
from .models import Pet
from random import randint

# @celery.decorators.periodic_task(run_every=crontab(hour=13, minute=17))
@celery.decorators.periodic_task(run_every=datetime.timedelta(hours=1))
def decrease_pet_stats():
	print("Decreasing pet stats...")
	for pet in Pet.objects.all():
		decrease_hunger = randint(0, 12) # about twice a day
		decrease_wellness = randint(0, 72) # once a day, but once every 3 days getting sick
		decrease_happiness = randint(0, 12)  # about twice a day

		if decrease_hunger == 12:
			if pet.hunger > 1:
				pet.hunger -= 1
		if decrease_wellness == 72:
			subject = "Oh No!"
			text = "Your pet has become very ill. It is recommended that you take them to the hospital."
			if pet.user:
				message = Message.objects.create(receiving_user=pet.user, subject=subject, text=text)
			pet.wellness = 1
		elif decrease_wellness > 68:
			if pet.wellness > 1:
				pet.wellness -= 1
		if decrease_happiness == 12:
			if pet.happiness > 1:
				pet.happiness -= 1

		pet.save()