from django.urls import re_path
from utils.error import error_page
from . import views

urlpatterns = [
    # static
    re_path(r"^$", views.home_page, name="home_page"),
    re_path(r"^error/$", error_page, name="error_page"),
    re_path(r"^colors/$", views.colors_page, name="colors_page"),
    re_path(r"^rules/$", views.rules_page, name="rules_page"),
    re_path(r"^privacy/$", views.privacy_policy_page, name="privacy_policy_page"),
    # users
    re_path(
        r"^profile/(?P<username>[\w-]+)/$",
        views.profile_page,
        name="profile_page",
    ),
    re_path(r"^profile/bio/edit/$", views.edit_bio, name="edit_bio"),
    re_path(r"^settings/$", views.settings_page, name="settings_page"),
    re_path(r"^settings/password/$", views.change_password, name="change_password"),
    re_path(
        r"^settings/view/$",
        views.change_view_settings,
        name="change_view_settings",
    ),
    re_path(
        r"^settings/friend-requests/$",
        views.change_friend_request_settings,
        name="change_friend_request_settings",
    ),
    re_path(
        r"^profile/(?P<username>[\w-]+)/block/$",
        views.block_user,
        name="block_user",
    ),
    re_path(
        r"^profile/(?P<username>[\w-]+)/unblock/$",
        views.unblock_user,
        name="unblock_user",
    ),
    re_path(r"^online/$", views.users_online_page, name="users_online_page"),
    # friends
    re_path(r"^friends/$", views.friends_page, name="friends_page"),
    re_path(
        r"^friends/(?P<username>[\w-]+)/send/$",
        views.send_friend_request,
        name="send_friend_request",
    ),
    re_path(
        r"^friends/(?P<username>[\w-]+)/accept/$",
        views.accept_friend_request,
        name="accept_friend_request",
    ),
    re_path(
        r"^friends/(?P<username>[\w-]+)/reject/$",
        views.reject_friend_request,
        name="reject_friend_request",
    ),
    re_path(
        r"^friends/(?P<username>[\w-]+)/remove/$",
        views.remove_friend,
        name="remove_friend",
    ),
    # registration
    re_path(r"^register/$", views.register_page, name="register_page"),
    re_path(r"^register/processing/$", views.register, name="register"),
    re_path(
        r"^register/success/$",
        views.successful_register_page,
        name="successful_register_page",
    ),
    # login/out
    re_path(r"^login/$", views.login_page, name="login_page"),
    re_path(r"^login/processing/$", views.login, name="login"),
    re_path(r"^logout/$", views.logout, name="logout"),
    re_path(r"^bonus/$", views.claim_login_bonus, name="claim_login_bonus"),
    re_path(
        r"^bonus/claimed/$",
        views.claimed_login_bonus_page,
        name="claimed_login_bonus_page",
    ),
    # pets
    re_path(r"^pet/$", views.change_pet_page, name="change_pet_page"),
    re_path(r"^pet/change/$", views.change_pet, name="change_pet"),
    re_path(r"^create/$", views.create_pet_step_1, name="create_pet_step_1"),
    re_path(
        r"^create/(?P<animal>[A-Za-z]+)/$",
        views.create_pet_step_2,
        name="create_pet_step_2",
    ),
    re_path(
        r"^create/(?P<animal>[A-Za-z]+)/name/$",
        views.create_pet_step_3,
        name="create_pet_step_3",
    ),
    re_path(r"^creating/$", views.create_pet, name="create_pet"),
    re_path(
        r"^creating/success/$",
        views.successful_create_pet_page,
        name="successful_create_pet_page",
    ),
]
