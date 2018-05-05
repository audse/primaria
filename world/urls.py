from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^world/$', views.world_page, name='world_page'),

    url(r'^garden/$', views.garden_page, name='garden_page'),
    url(r'^garden/gather/$', views.garden_gather, name='garden_gather'),

    url(r'^hospital/$', views.hospital_page, name='hospital_page'),
    url(r'^hospital/appointment/$', views.make_hospital_appointment, name='make_hospital_appointment'),
    url(r'^hospital/pickup/$', views.pickup_hospital_medicine, name='pickup_hospital_medicine'),

    url(r'^pound/$', views.pound_page, name='pound_page'),
    url(r'^pound/release/$', views.give_up_pet, name='give_up_pet'),
    url(r'^pound/adopt/(?P<adopt>[\w-]+)$', views.adopt_from_pound, name='adopt_from_pound'),

    url(r'^games/$', views.games_page, name='games_page'),
    url(r'^games/blackjack/$', views.blackjack_page, name='blackjack_page'),
    url(r'^games/tictactoe/$', views.tictactoe_page, name='tictactoe_page'),
    url(r'^games/pyramids/$', views.pyramids_page, name='pyramids_page'),
    url(r'^games/wheel/serendipity/$', views.wheel_serendipity_page, name='wheel_serendipity_page'),
    url(r'^games/wheel/plush/$', views.wheel_plush_page, name='wheel_plush_page'),
    url(r'^games/(?P<game>[A-Za-z]+)/send/$', views.send_score, name='send_score'),

    url(r'fishing/$', views.fishing_page, name='fishing_page'),
    url(r'fishing/purchase/rod/$', views.purchase_rod, name='purchase_rod'),
    url(r'fishing/purchase/upgrade/$', views.upgrade_rod, name='upgrade_rod'),
    url(r'fishing/purchase/bait/$', views.purchase_bait, name='purchase_bait'),
    url(r'fishing/fish/$', views.fish, name='fish'),
    url(r'fishing/(?P<pk>[0-9]+)/sell/$', views.sell_fish, name='sell_fish'),

    url(r'dump/$', views.dump_page, name='dump_page'),
    url(r'dump/(?P<pk>[0-9]+)/take/$', views.take_from_dump, name='take_from_dump'),
    url(r'dump/add/$', views.dump_item, name='dump_item'),

    url(r'quarry/$', views.quarry_page, name='quarry_page'),
    url(r'quarry/purchase/rod/$', views.purchase_dowsing_rod, name='purchase_dowsing_rod'),
    url(r'quarry/upgrade/rod/$', views.upgrade_dowsing_rod, name='upgrade_dowsing_rod'),
    url(r'quarry/dowse/$', views.dowse, name='dowse'),
    url(r'quarry/trade/(?P<crystal>[\w-]+)/$', views.trade_crystals, name='trade_crystals'),

    url(r'restricted/$', views.restricted_area_page, name='restricted_area_page'),
    url(r'restricted/update/(?P<crystal>[\w-]+)/$', views.update_card, name='update_card'),
    url(r'restricted/activate/$', views.activate_card, name='activate_card'),
    url(r'restricted/machine/$', views.restricted_machine, name='restricted_machine'),


    # DAILIES

    url(r'meatloaf/$', views.almighty_meatloaf_page, name='almighty_meatloaf_page'),
    url(r'meatloaf/take/$', views.take_from_meatloaf, name='take_from_meatloaf'),

    url(r'trails/$', views.trails_page, name='trails_page'),
    url(r'trails/run/$', views.trails, name='trails'),

    url(r'orchard/$', views.apple_orchard_page, name='apple_orchard_page'),
    url(r'orchard/take/$', views.apple_orchard, name='apple_orchard'),

    url(r'day-old/$', views.day_old_stock_page, name='day_old_stock_page'),
    url(r'day-old/take/$', views.day_old_stock, name='day_old_stock'),

    url(r'vending/$', views.vending_machine_page, name='vending_machine_page'),
    url(r'vending/(?P<pk>[0-9]+)/vend/$', views.vending_machine, name='vending_machine'),
]
