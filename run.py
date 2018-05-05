# empty
# run execfile('run.py') to run in python manage.py shell
# exit() to exit shell

# KEEP #

from shop.models import Item, Category

basic_animals = ["dino", "lizard", "monkey", "mouse", "tapir"]
basic_colors = ["red", "yellow", "green", "blue", "black"]

special_animals = ["bird", "crab", "dog", "gargoyle", "penguin"]
special_colors = ["albino", "baroque", "black-knit", "blue-knit", "camo", "cloud", "galaxy", "gingham", "glitter", "green-knit", "iridescent", "iridescent", "marble", "opalescent", "pink", "red-knit", "sea", "sprinkle", "starry", "tiger", "yellow-knit"]

# ENDKEEP #

cat = Category.objects.create(name="candy")

candies_names = ["Hershel Smooches", "Jolly Broncos", "Lollipop", "N n N's", "Simplies"]
candies_urls = ["hershel-smooches", "jolly-broncos", "lollipop", "n-n-ns", "simplies"]
candies_prices = [2, 1, 1, 1, 2]

n = 0
while n < 5:
	item = Item.objects.create(name=candies_names[n], url=candies_urls[n], category=Category.objects.get(name="junk food"), second_category=Category.objects.get(name="candy"), description="TBA", price_class=candies_prices[n], rarity=1, hunger=10, happiness=10)
	n += 1