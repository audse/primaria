from django.template import Library
from social.models import Message

register = Library()

@register.filter(name="get_messages")
def get_messages(user):
	messages = Message.objects.filter(receiving_user=user, read=False, deleted_by_receiver=False).count()
	return messages
