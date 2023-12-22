from django.conf.urls import url

urlpatterns = [
    url(r"^world/$", "world.views.world_page", name="world_page"),
    url(r"^garden/$", "world.views.garden_page", name="garden_page"),
    url(r"^garden/gather/$", "world.views.garden_gather", name="garden_gather"),
    url(r"^hospital/$", "world.views.hospital_page", name="hospital_page"),
    url(
        r"^hospital/appointment/$",
        "world.views.make_hospital_appointment",
        name="make_hospital_appointment",
    ),
    url(
        r"^hospital/pickup/$",
        "world.views.pickup_hospital_medicine",
        name="pickup_hospital_medicine",
    ),
    url(r"^pound/$", "world.views.pound_page", name="pound_page"),
    url(r"^pound/release/$", "world.views.give_up_pet", name="give_up_pet"),
    url(
        r"^pound/adopt/(?P<adopt>[\w-]+)$",
        "world.views.adopt_from_pound",
        name="adopt_from_pound",
    ),
    url(r"^games/$", "world.views.games_page", name="games_page"),
    url(r"^games/blackjack/$", "world.views.blackjack_page", name="blackjack_page"),
    url(r"^games/tictactoe/$", "world.views.tictactoe_page", name="tictactoe_page"),
    url(r"^games/pyramids/$", "world.views.pyramids_page", name="pyramids_page"),
    url(
        r"^games/wheel/serendipity/$",
        "world.views.wheel_serendipity_page",
        name="wheel_serendipity_page",
    ),
    url(
        r"^games/wheel/plush/$", "world.views.wheel_plush_page", name="wheel_plush_page"
    ),
    url(
        r"^games/(?P<game>[A-Za-z]+)/send/$",
        "world.views.send_score",
        name="send_score",
    ),
    url(r"fishing/$", "world.views.fishing_page", name="fishing_page"),
    url(r"fishing/purchase/rod/$", "world.views.purchase_rod", name="purchase_rod"),
    url(r"fishing/purchase/upgrade/$", "world.views.upgrade_rod", name="upgrade_rod"),
    url(r"fishing/purchase/bait/$", "world.views.purchase_bait", name="purchase_bait"),
    url(r"fishing/fish/$", "world.views.fish", name="fish"),
    url(r"fishing/(?P<pk>[0-9]+)/sell/$", "world.views.sell_fish", name="sell_fish"),
    url(r"dump/$", "world.views.dump_page", name="dump_page"),
    url(
        r"dump/(?P<pk>[0-9]+)/take/$",
        "world.views.take_from_dump",
        name="take_from_dump",
    ),
    url(r"dump/add/$", "world.views.dump_item", name="dump_item"),
    url(r"quarry/$", "world.views.quarry_page", name="quarry_page"),
    url(
        r"quarry/purchase/rod/$",
        "world.views.purchase_dowsing_rod",
        name="purchase_dowsing_rod",
    ),
    url(
        r"quarry/upgrade/rod/$",
        "world.views.upgrade_dowsing_rod",
        name="upgrade_dowsing_rod",
    ),
    url(r"quarry/dowse/$", "world.views.dowse", name="dowse"),
    url(
        r"quarry/trade/(?P<crystal>[\w-]+)/$",
        "world.views.trade_crystals",
        name="trade_crystals",
    ),
    url(
        r"restricted/$", "world.views.restricted_area_page", name="restricted_area_page"
    ),
    url(
        r"restricted/update/(?P<crystal>[\w-]+)/$",
        "world.views.update_card",
        name="update_card",
    ),
    url(r"restricted/activate/$", "world.views.activate_card", name="activate_card"),
    url(
        r"restricted/machine/$",
        "world.views.restricted_machine",
        name="restricted_machine",
    ),
    # DAILIES
    url(
        r"meatloaf/$",
        "world.views.almighty_meatloaf_page",
        name="almighty_meatloaf_page",
    ),
    url(
        r"meatloaf/take/$", "world.views.take_from_meatloaf", name="take_from_meatloaf"
    ),
    url(r"trails/$", "world.views.trails_page", name="trails_page"),
    url(r"trails/run/$", "world.views.trails", name="trails"),
    url(r"orchard/$", "world.views.apple_orchard_page", name="apple_orchard_page"),
    url(r"orchard/take/$", "world.views.apple_orchard", name="apple_orchard"),
    url(r"day-old/$", "world.views.day_old_stock_page", name="day_old_stock_page"),
    url(r"day-old/take/$", "world.views.day_old_stock", name="day_old_stock"),
    url(r"vending/$", "world.views.vending_machine_page", name="vending_machine_page"),
    url(
        r"vending/(?P<pk>[0-9]+)/vend/$",
        "world.views.vending_machine",
        name="vending_machine",
    ),
]
