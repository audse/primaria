from django.shortcuts import render, redirect

from core.models import Pet, Avatar
from social.models import Message
from world.models import DailyClaim
from shop.models import Category, Item, Inventory
from utils.error import error_page

from .models import Quest

from datetime import datetime
import random

def goddess_neglect_page(request):
	if request.user.is_authenticated():
		pet = Pet.objects.filter(user=request.user).first()
		today = datetime.today()
		claims = DailyClaim.objects.filter(user=request.user, daily_type="neglect", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).first()
		maximum = False
		if pet:
			if pet.hunger >= 3 and pet.wellness >= 4 and pet.happiness >= 3:
				maximum = True

		unfinished_quest = Quest.objects.filter(user=request.user, goddess="neglect", completed=False).first()
		quests_today = Quest.objects.filter(user=request.user, goddess="neglect", completed=True, date__year=today.year, date__month=today.month, date__day=today.day).count()
		completed = request.session.pop('completed', False)
		return render(request, 'goddess/neglect_page.html', {'pet':pet, 'maximum':maximum, 'claims':claims, 'unfinished_quest':unfinished_quest, 'quests_today':quests_today, 'completed':completed})
	else:
		request.session['error'] = "You must be logged in to view this page."
		return redirect(error_page)

def goddess_sun_page(request):
	if request.user.is_authenticated():
		today = datetime.today()

		unfinished_quest = Quest.objects.filter(user=request.user, goddess="sun", completed=False).first()
		quests_today = Quest.objects.filter(user=request.user, goddess="sun", date__year=today.year, date__month=today.month, date__day=today.day).count()
		completed = request.session.pop('completed', False)
		return render(request, 'goddess/sun_page.html', {'unfinished_quest':unfinished_quest, 'quests_today':quests_today, 'completed':completed})
	else:
		request.session['error'] = "You must be logged in to view this page."
		return redirect(error_page)

def goddess_garden_page(request):
	if request.user.is_authenticated():
		today = datetime.today()

		unfinished_quest = Quest.objects.filter(user=request.user, goddess="garden", completed=False).first()
		quests_today = Quest.objects.filter(user=request.user, goddess="garden", date__year=today.year, date__month=today.month, date__day=today.day).count()
		completed = request.session.pop('completed', False)
		return render(request, 'goddess/garden_page.html', {'unfinished_quest':unfinished_quest, 'quests_today':quests_today, 'completed':completed})
	else:
		request.session['error'] = "You must be logged in to view this page."
		return redirect(error_page)

def goddess_ocean_page(request):
	if request.user.is_authenticated():
		today = datetime.today()

		unfinished_quest = Quest.objects.filter(user=request.user, goddess="ocean", completed=False).first()
		quests_today = Quest.objects.filter(user=request.user, goddess="ocean", date__year=today.year, date__month=today.month, date__day=today.day).count()
		completed = request.session.pop('completed', False)
		return render(request, 'goddess/ocean_page.html', {'unfinished_quest':unfinished_quest, 'quests_today':quests_today, 'completed':completed})
	else:
		request.session['error'] = "You must be logged in to view this page."
		return redirect(error_page)

def goddess_commerce_page(request):
	if request.user.is_authenticated():
		today = datetime.today()

		unfinished_quest = Quest.objects.filter(user=request.user, goddess="commerce", completed=False).first()
		quests_today = Quest.objects.filter(user=request.user, goddess="commerce", date__year=today.year, date__month=today.month, date__day=today.day).count()
		completed = request.session.pop('completed', False)

		# QUEST
		deactivated_card = Item.objects.get(url="deactivated-bank-card")
		deactivated_card = Inventory.objects.filter(item=deactivated_card, user=request.user, box=False, pending=False).first()
		activated_card = Item.objects.get(url="activated-area-card")
		activated_card = Inventory.objects.filter(item=activated_card, user=request.user, box=False, pending=False).first()

		return render(request, 'goddess/commerce_page.html', {'unfinished_quest':unfinished_quest, 'quests_today':quests_today, 'completed':completed, 'deactivated_card':deactivated_card, 'activated_card':activated_card})
	else:
		request.session['error'] = "You must be logged in to view this page."
		return redirect(error_page)

def goddess_neglect_collect(request):
	if request.user.is_authenticated():
		pet = Pet.objects.filter(user=request.user).first()
		if pet:
			today = datetime.today()
			claims = DailyClaim.objects.filter(user=request.user, daily_type="neglect", date_of_claim__year=today.year, date_of_claim__month=today.month, date_of_claim__day=today.day).count()
			if claims == 0:
				if pet.hunger >= 3 and pet.wellness >= 4 and pet.happiness >= 3:
					# food_or_herb = random.randint(1, 2)
					# if food_or_herb == 1:
					# 	food_category = Category.objects.filter(name="organic food").first()
					# 	foods = Item.objects.filter(category=food_category, rarity=3) | Item.objects.filter(second_category=food_category, rarity=3)
					# 	food = random.choice(foods)
					# 	message = "Thank you for keeping your pet happy and healthy! You have received a " + food.name + " as a reward."
					# 	items_in_inventory = Inventory.objects.filter(user=request.user, box=False, pending=False).count()
					# 	if items_in_inventory < 50:
					# 		inventory = Inventory.objects.create(user=request.user, item=food)
					# 	else:
					# 		message += "But your bag is full! You gave it back."
					# 	claim = DailyClaim.objects.create(user=request.user, daily_type="neglect", message=message, reward=food)
					# 	return redirect(goddess_neglect_page)
					# elif food_or_herb == 2:
					# 	herb_category = Category.objects.filter(name="herbal").first()
					# 	herbs = Item.objects.filter(category=herb_category, rarity=2) | Item.objects.filter(second_category=herb_category, rarity=2)
					# 	herb = random.choice(herbs)
					# 	message = "Thank you for keeping your pet happy and healthy! You have received a " + herb.name + " as a reward."
					# 	items_in_inventory = Inventory.objects.filter(user=request.user, box=False, pending=False).count()
					# 	if items_in_inventory < 50:
					# 		inventory = Inventory.objects.create(user=request.user, item=herb)
					# 	else:
					# 		message += "But your bag is full! You gave it back."
					# 	claim = DailyClaim.objects.create(user=request.user, daily_type="neglect", message=message, reward=herb)
					# 	return redirect(goddess_neglect_page)
					if Inventory.objects.filter(user=request.user, box=False, pending=False).count() < 50:
						prize_type = random.randint(1, 4)
						if prize_type == 1: # random stat potion
							reward = Item.objects.filter(second_category=Category.objects.get(name="stat potion")).order_by('?').first()
							message = "Thank you for keeping your pet happy and healthy! You have received a " + reward.name + " as a reward."
							inventory = Inventory.objects.create(user=request.user, item=reward)
							claim = DailyClaim.objects.create(user=request.user, daily_type="neglect", message=message, reward=reward)
							return redirect(goddess_neglect_page)
						elif prize_type == 2: # random prescription medicine
							reward = Item.objects.filter(category=Category.objects.get(name="medicine")).order_by('?').first()
							message = "Thank you for keeping your pet happy and healthy! You have received a " + reward.name + " as a reward."
							inventory = Inventory.objects.create(user=request.user, item=reward)
							claim = DailyClaim.objects.create(user=request.user, daily_type="neglect", message=message, reward=reward)
							return redirect(goddess_neglect_page)
						elif prize_type == 3: # random rare plush
							reward = Item.objects.filter(category=Category.objects.get(name="plush"), rarity__gte=2).order_by('?').first()
							message = "Thank you for keeping your pet happy and healthy! You have received a " + reward.name + " as a reward."
							inventory = Inventory.objects.create(user=request.user, item=reward)
							claim = DailyClaim.objects.create(user=request.user, daily_type="neglect", message=message, reward=reward)
							return redirect(goddess_neglect_page)
						elif prize_type == 4: # random 3 items (hunger, wellness, happiness)
							if Inventory.objects.filter(user=request.user, box=False, pending=False).count() < 48:
								hunger_reward = Item.objects.filter(second_category=Category.objects.get(name="organic food"), rarity__lte=2).order_by('?').first()
								wellness_reward = Item.objects.filter(category=Category.objects.get(name="herbal"), rarity__lte=2).order_by('?').first()
								happiness_reward = Item.objects.filter(category=Category.objects.get(name="book"), rarity=1).order_by('?').first()
								message = "Thank you for keeping your pet happy and healthy! You have received a " + hunger_reward.name + ", a " + wellness_reward.name + ", and a " + happiness_reward.name + " as a reward."
								inventory = Inventory.objects.create(user=request.user, item=hunger_reward)
								inventory = Inventory.objects.create(user=request.user, item=wellness_reward)
								inventory = Inventory.objects.create(user=request.user, item=happiness_reward)
								claim = DailyClaim.objects.create(user=request.user, daily_type="neglect", message=message)
								return redirect(goddess_neglect_page)
							else:
								request.session['error'] = "You can only have up to 50 items in your inventory."
								return redirect(error_page)
					else:
						request.session['error'] = "You can only have up to 50 items in your inventory."
						return redirect(error_page)
				else:
					request.session['error'] = "You have already claimed your gift for today."
					return redirect(error_page)
			else:
				request.session['error'] = "Your pet must be at maximum stats to receive a gift from the Goddess of Neglect."
				return redirect(error_page)
		else:
			request.session['error'] = "You must have a pet to view this page."
			return redirect(error_page)
	else:
		request.session['error'] = "You must be logged in to view this page."
		return redirect(error_page)

def start_goddess_quest(request, goddess):
	if request.user.is_authenticated():
		today = datetime.today()
		unfinished_quests = Quest.objects.filter(user=request.user, goddess=goddess, completed=False).count()
		quests_today = Quest.objects.filter(user=request.user, goddess=goddess, completed=True, date__year=today.year, date__month=today.month, date__day=today.day).count()
		if unfinished_quests < 1:
			if quests_today < 5:
				requested_item = None
				reward_item = None
				reward_points = None

				if goddess == "neglect":
					item_category = Category.objects.get(name="plush")
				elif goddess == "ocean":
					item_category = Category.objects.get(name="fruit")
				elif goddess == "garden":
					item_category = Category.objects.get(name="vegetable")
				elif goddess == "commerce":
					item_category = Category.objects.get(name="playing card")
				elif goddess == "sun":
					item_category = Category.objects.get(name="crystal")
				else:
					request.session['error'] = "No goddess with that name exists."
					return redirect(error_page)

				difficulty = random.randint(1, 3)
				potion_category = Category.objects.get(name="potion")
				crystal_category = Category.objects.get(name="crystal")
				area_card_category = Category.objects.get(name="area card")
				if difficulty == 1:
					requested_item = Item.objects.exclude(category=potion_category).exclude(category=crystal_category).exclude(category=area_card_category).filter(rarity=1).order_by('?').first()
					reward_points = random.randint(250, 500)
				elif difficulty == 2:
					requested_item = Item.objects.exclude(category=potion_category).exclude(category=crystal_category).exclude(category=area_card_category).filter(rarity=2).order_by('?').first()
					reward_points = random.randint(600, 1000)
				elif difficulty == 3:
					requested_item = Item.objects.exclude(category=potion_category).exclude(category=crystal_category).exclude(category=area_card_category).filter(rarity=3).order_by('?').first()
					reward_points = random.randint(900, 2500)

				prize_type = random.randint(1, 3)
				if prize_type == 1: # only item
					if goddess != "sun":
						reward_item = Item.objects.filter(category=item_category, rarity=2).order_by('?').first()
						reward_points = None
					else: # get only small crystals
						reward_item = Item.objects.filter(name__icontains="small", category=item_category, rarity=2).order_by('?').first()
				elif prize_type == 2: # only points
					reward_item = None
				elif prize_type == 3: # item and points
					if goddess != "sun":
						reward_item = Item.objects.filter(category=item_category, rarity=1).order_by('?').first()
					else:
						reward_item = Item.objects.filter(name__icontains="small", category=item_category, rarity=2).order_by('?').first()
					reward_points -= 150
				quest = Quest.objects.create(user=request.user, goddess=goddess, requested_item=requested_item, reward_item=reward_item, reward_points=reward_points)

				if goddess == "neglect":
					return redirect(goddess_neglect_page)
				elif goddess == "garden":
					return redirect(goddess_garden_page)
				elif goddess == "ocean":
					return redirect(goddess_ocean_page)
				elif goddess == "commerce":
					return redirect(goddess_commerce_page)
				elif goddess == "sun":
					return redirect(goddess_sun_page)
				else:
					return redirect(error_page)
			else:
				request.session['error'] = "You have already completed the maximum quests for this Goddess today."
				return redirect(error_page)
		else:
			request.session['error'] = "You cannot start a new quest if you haven't completed or cancelled the current one."
			return redirect(error_page)
	else:
		request.session['error'] = "You must be logged in to view this page."
		return redirect(error_page)

def complete_goddess_quest(request, goddess):
	if request.user.is_authenticated():
		quest = Quest.objects.filter(user=request.user, goddess=goddess, completed=False).first()
		if quest:
			item = Inventory.objects.filter(user=request.user, item=quest.requested_item, box=False, pending=False).first()
			if item:
				if quest.reward_item:
					reward_item = Inventory.objects.create(user=request.user, item=quest.reward_item)
				if quest.reward_points:
					request.user.profile.points += quest.reward_points
					request.user.profile.save()
				item.delete()
				quest.completed = True
				quest.save()


				# AVATARS
				today = datetime.today()
				divine_avatar = Avatar.objects.get(url="divine")
				if divine_avatar not in request.user.profile.avatars.all():
					new_quest_count = Quest.objects.filter(user=request.user, completed=True, cancelled=False, date__year=today.year, date__month=today.month, date__day=today.day).count()
					if new_quest_count >= 20:
						request.user.profile.avatars.add(divine_avatar)
						request.user.profile.save()
						message = Message.objects.create(receiving_user=request.user, subject="You just found a secret avatar!", text="You have just received the avatar \"Divine\" to use on the boards!")

				request.session['completed'] = "You have completed your quest! Check your inventory and/or points for your reward." 
				if goddess == "neglect":
					return redirect(goddess_neglect_page)
				elif goddess == "garden":
					return redirect(goddess_garden_page)
				elif goddess == "ocean":
					return redirect(goddess_ocean_page)
				elif goddess == "commerce":
					return redirect(goddess_commerce_page)
				elif goddess == "sun":
					return redirect(goddess_sun_page)
			else:
				request.session['error'] = "You do not have the item you need to complete your quest."
				return redirect(error_page)
		else:
			request.session['error'] = "You do not have a quest to complete."
			return redirect(error_page)
	else:
		request.session['error'] = "You must be logged in to view this page."
		return redirect(error_page)

def cancel_goddess_quest(request, goddess):
	if request.user.is_authenticated():
		quest = Quest.objects.filter(user=request.user, goddess=goddess, completed=False).first()
		if quest:
			quest.completed = True
			quest.cancelled = True
			quest.save()
			if goddess == "neglect":
				request.session['completed'] = "You have cancelled your quest." 
				return redirect(goddess_neglect_page)
			elif goddess == "garden":
				return redirect(goddess_garden_page)
			elif goddess == "ocean":
				return redirect(goddess_ocean_page)
			elif goddess == "commerce":
				return redirect(goddess_commerce_page)
			elif goddess == "sun":
				return redirect(goddess_sun_page)
		else:
			request.session['error'] = "You do not have a quest to complete."
			return redirect(error_page)
	else:
		request.session['error'] = "You must be logged in to view this page."
		return redirect(error_page)








