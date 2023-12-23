from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^messages/$", views.messages_page, name="messages_page"),
    re_path(
        r"^messages/read/(?P<pk>[0-9]+)/$",
        views.mark_message_as_read,
        name="mark_message_as_read",
    ),
    re_path(
        r"^messages/unread/(?P<pk>[0-9]+)/$",
        views.mark_message_as_unread,
        name="mark_message_as_unread",
    ),
    re_path(r"^messages/send/$", views.send_message, name="send_message"),
    re_path(
        r"^messages/delete/(?P<pk>[0-9]+)/$",
        views.delete_message,
        name="delete_message",
    ),
    re_path(r"^boards/$", views.boards_page, name="boards_page"),
    re_path(r"^boards/(?P<board>[\w-]+)/$", views.board_page, name="board_page"),
    re_path(
        r"^boards/topic/(?P<topic>[\w-]+)/$",
        views.topic_page,
        name="topic_page",
    ),
    re_path(
        r"^boards/avatar/(?P<avatar>[\w-]+)/$",
        views.change_avatar,
        name="change_avatar",
    ),
    re_path(r"^boards/post/processing/$", views.post_topic, name="post_topic"),
    re_path(
        r"^boards/reply/processing/$",
        views.reply_to_topic,
        name="reply_to_topic",
    ),
    re_path(
        r"^boards/topic/(?P<topic>[\w-]+)/lock/$",
        views.lock_topic,
        name="lock_topic",
    ),
    re_path(
        r"^boards/topic/(?P<topic>[\w-]+)/unlock/$",
        views.unlock_topic,
        name="unlock_topic",
    ),
    re_path(
        r"^boards/topic/(?P<topic>[\w-]+)/delete/$",
        views.delete_topic,
        name="delete_topic",
    ),
    re_path(
        r"^boards/topic/(?P<topic>[\w-]+)/undelete/$",
        views.undelete_topic,
        name="undelete_topic",
    ),
    re_path(
        r"^boards/topic/(?P<topic>[\w-]+)/sticky/$",
        views.sticky_topic,
        name="sticky_topic",
    ),
    re_path(
        r"^boards/topic/(?P<topic>[\w-]+)/unsticky/$",
        views.unsticky_topic,
        name="unsticky_topic",
    ),
    re_path(r"^boards/reply/delete/$", views.delete_reply, name="delete_reply"),
    re_path(
        r"^boards/reply/(?P<reply>[0-9]+)/undelete/$",
        views.undelete_reply,
        name="undelete_reply",
    ),
]
