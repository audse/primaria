from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^messages/$', views.messages_page, name='messages_page'),
    url(r'^messages/read/(?P<pk>[0-9]+)/$', views.mark_message_as_read, name='mark_message_as_read'),
    url(r'^messages/unread/(?P<pk>[0-9]+)/$', views.mark_message_as_unread, name='mark_message_as_unread'),
    url(r'^messages/send/$', views.send_message, name='send_message'),
    url(r'^messages/delete/(?P<pk>[0-9]+)/$', views.delete_message, name='delete_message'),

    url(r'^boards/$', views.boards_page, name='boards_page'),
    url(r'^boards/(?P<board>[\w-]+)/$', views.board_page, name='board_page'),
    url(r'^boards/topic/(?P<topic>[\w-]+)/$', views.topic_page, name='topic_page'),
    url(r'^boards/avatar/(?P<avatar>[\w-]+)/$', views.change_avatar, name='change_avatar'),

    url(r'^boards/post/processing/$', views.post_topic, name='post_topic'),
    url(r'^boards/reply/processing/$', views.reply_to_topic, name='reply_to_topic'),

    url(r'^boards/topic/(?P<topic>[\w-]+)/lock/$', views.lock_topic, name='lock_topic'),
    url(r'^boards/topic/(?P<topic>[\w-]+)/unlock/$', views.unlock_topic, name='unlock_topic'),
    url(r'^boards/topic/(?P<topic>[\w-]+)/delete/$', views.delete_topic, name='delete_topic'),
    url(r'^boards/topic/(?P<topic>[\w-]+)/undelete/$', views.undelete_topic, name='undelete_topic'),
    url(r'^boards/topic/(?P<topic>[\w-]+)/sticky/$', views.sticky_topic, name='sticky_topic'),
    url(r'^boards/topic/(?P<topic>[\w-]+)/unsticky/$', views.unsticky_topic, name='unsticky_topic'),
    url(r'^boards/reply/delete/$', views.delete_reply, name='delete_reply'),
    url(r'^boards/reply/(?P<reply>[0-9]+)/undelete/$', views.undelete_reply, name='undelete_reply'),
]