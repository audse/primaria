from django.contrib import admin

from .models import Message, Badge, Board, Topic, Reply

admin.site.register(Message)
admin.site.register(Badge)
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Reply)
