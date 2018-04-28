from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^error/$', views.error_page, name='error_page'),
    url(r'^profile/(?P<username>[\w-]+)/$', views.profile_page, name='profile_page'),
    url(r'^profile/bio/edit/$', views.edit_bio, name='edit_bio'),
    url(r'^pet/$', views.change_pet_page, name='change_pet_page'),
    url(r'^pet/change/$', views.change_pet, name='change_pet'),
    url(r'^settings/$', views.settings_page, name='settings_page'),
    url(r'^settings/password/$', views.change_password, name='change_password'),
    url(r'^settings/view/$', views.change_view_settings, name='change_view_settings'),

    # registration
    url(r'^register/$', views.register_page, name='register_page'),
    url(r'^register/processing/$', views.register, name='register'),
    url(r'^register/success/$', views.successful_register_page, name='successful_register_page'),

    # login/out
    url(r'^login/$', views.login_page, name='login_page'),
    url(r'^login/processing/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    # features
    url(r'^create/$', views.create_pet_step_1, name='create_pet_step_1'),
    url(r'^create/(?P<animal>[A-Za-z]+)/$', views.create_pet_step_2, name='create_pet_step_2'),
    url(r'^create/(?P<animal>[A-Za-z]+)/name/$', views.create_pet_step_3, name='create_pet_step_3'),
    url(r'^creating/$', views.create_pet, name='create_pet'),
    url(r'^creating/success/$', views.successful_create_pet_page, name='successful_create_pet_page'),

    url(r'^colors/$', views.colors_page, name='colors_page'),
    url(r'^online/$', views.users_online_page, name='users_online_page'),
    url(r'^rules/$', views.rules_page, name='rules_page'),
    url(r'^privacy/$', views.privacy_policy_page, name='privacy_policy_page'),

    url(r'^profile/(?P<username>[\w-]+)/block/$', views.block_user, name='block_user'),
    url(r'^profile/(?P<username>[\w-]+)/unblock/$', views.unblock_user, name='unblock_user'),

    url(r'^bonus/$', views.claim_login_bonus, name='claim_login_bonus'),
    url(r'^bonus/claimed/$', views.claimed_login_bonus_page, name='claimed_login_bonus_page'),

]
