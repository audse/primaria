from django.conf.urls import url, include
from django.contrib import admin

from core import views
from utils.error import error_page

urlpatterns = [
    # static
    url(r"^$", "core.views.home_page", name="home_page"),
    url(r"^error/$", error_page, name="error_page"),
    url(r"^colors/$", "core.views.colors_page", name="colors_page"),
    url(r"^rules/$", "core.views.rules_page", name="rules_page"),
    url(r"^privacy/$", "core.views.privacy_policy_page", name="privacy_policy_page"),
    # users
    url(
        r"^profile/(?P<username>[\w-]+)/$",
        "core.views.profile_page",
        name="profile_page",
    ),
    url(r"^profile/bio/edit/$", "core.views.edit_bio", name="edit_bio"),
    url(r"^settings/$", "core.views.settings_page", name="settings_page"),
    url(r"^settings/password/$", "core.views.change_password", name="change_password"),
    url(
        r"^settings/view/$",
        "core.views.change_view_settings",
        name="change_view_settings",
    ),
    url(
        r"^settings/friend-requests/$",
        "core.views.change_friend_request_settings",
        name="change_friend_request_settings",
    ),
    url(
        r"^profile/(?P<username>[\w-]+)/block/$",
        "core.views.block_user",
        name="block_user",
    ),
    url(
        r"^profile/(?P<username>[\w-]+)/unblock/$",
        "core.views.unblock_user",
        name="unblock_user",
    ),
    url(r"^online/$", "core.views.users_online_page", name="users_online_page"),
    # friends
    url(r"^friends/$", "core.views.friends_page", name="friends_page"),
    url(
        r"^friends/(?P<username>[\w-]+)/send/$",
        "core.views.send_friend_request",
        name="send_friend_request",
    ),
    url(
        r"^friends/(?P<username>[\w-]+)/accept/$",
        "core.views.accept_friend_request",
        name="accept_friend_request",
    ),
    url(
        r"^friends/(?P<username>[\w-]+)/reject/$",
        "core.views.reject_friend_request",
        name="reject_friend_request",
    ),
    url(
        r"^friends/(?P<username>[\w-]+)/remove/$",
        "core.views.remove_friend",
        name="remove_friend",
    ),
    # registration
    url(r"^register/$", "core.views.register_page", name="register_page"),
    url(r"^register/processing/$", "core.views.register", name="register"),
    url(
        r"^register/success/$",
        "core.views.successful_register_page",
        name="successful_register_page",
    ),
    # login/out
    url(r"^login/$", "core.views.login_page", name="login_page"),
    url(r"^login/processing/$", "core.views.login", name="login"),
    url(r"^logout/$", "core.views.logout", name="logout"),
    url(r"^bonus/$", "core.views.claim_login_bonus", name="claim_login_bonus"),
    url(
        r"^bonus/claimed/$",
        "core.views.claimed_login_bonus_page",
        name="claimed_login_bonus_page",
    ),
    # pets
    url(r"^pet/$", "core.views.change_pet_page", name="change_pet_page"),
    url(r"^pet/change/$", "core.views.change_pet", name="change_pet"),
    url(r"^create/$", "core.views.create_pet_step_1", name="create_pet_step_1"),
    url(
        r"^create/(?P<animal>[A-Za-z]+)/$",
        "core.views.create_pet_step_2",
        name="create_pet_step_2",
    ),
    url(
        r"^create/(?P<animal>[A-Za-z]+)/name/$",
        "core.views.create_pet_step_3",
        name="create_pet_step_3",
    ),
    url(r"^creating/$", "core.views.create_pet", name="create_pet"),
    url(
        r"^creating/success/$",
        "core.views.successful_create_pet_page",
        name="successful_create_pet_page",
    ),
]
