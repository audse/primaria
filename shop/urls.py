from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^inventory/$', views.inventory_page, name='inventory_page'),
    url(r'^inventory/use/$', views.use_item, name='use_item'),
    url(r'^inventory/results/$', views.potion_results_page, name='potion_results_page'),

    url(r'^shop/(?P<shop_url>[A-Za-z,-]+)/$', views.shop_page, name='shop_page'),
    url(r'^shop/(?P<shop_url>[A-Za-z,-]+)/purchase/$', views.purchase_item, name='purchase_item'),

    url(r'^bank/$', views.bank_page, name='bank_page'),
    url(r'^bank/open/$', views.open_bank_account_page, name='open_bank_account_page'),
    url(r'^bank/open/processing/$', views.open_bank_account, name='open_bank_account'),
    url(r'^bank/deposit/$', views.deposit, name='deposit'),
    url(r'^bank/withdraw/$', views.withdraw, name='withdraw'),
    url(r'^bank/interest/$', views.collect_interest, name='collect_interest'),
    url(r'^bank/upgrade/$', views.upgrade_bank_account, name='upgrade_bank_account'),

    url(r'^gallery/$', views.gallery_page, name='gallery_page'),
    url(r'^gallery/open/$', views.open_gallery_page, name='open_gallery_page'),
    url(r'^gallery/open/processing/$', views.open_gallery, name='open_gallery'),
    url(r'^gallery/add/$', views.add_gallery_item, name='add_gallery_item'),
    url(r'^gallery/upgrade/$', views.upgrade_gallery, name='upgrade_gallery'),
    url(r'^gallery/rename/$', views.rename_gallery, name='rename_gallery'),

    url(r'^personal/shop/$', views.your_shop_page, name='your_shop_page'),
    url(r'^personal/shop/open/$', views.open_shop_page, name='open_shop_page'),
    url(r'^personal/shop/open/processing/$', views.open_shop, name='open_shop'),
    url(r'^personal/shop/add/$', views.add_shop_item, name='add_shop_item'),
    url(r'^personal/shop/edit/$', views.edit_price, name='edit_price'),
    url(r'^personal/shop/remove/$', views.remove_from_shop, name='remove_from_shop'),
    url(r'^personal/shop/withdraw/$', views.withdraw_shop_till, name='withdraw_shop_till'),
    url(r'^personal/shop/upgrade/$', views.upgrade_shop, name='upgrade_shop'),
    url(r'^personal/shop/rename/$', views.rename_shop, name='rename_shop'),

    url(r'^profile/(?P<username>[\w-]+)/shop/$', views.user_shop_page, name='user_shop_page'),
    url(r'^profile/(?P<username>[\w-]+)/gallery/$', views.user_gallery_page, name='user_gallery_page'),
    url(r'^profile/(?P<username>[\w-]+)/shop/purchase/$', views.purchase_from_user_shop, name='purchase_from_user_shop'),

    url(r'^search/shop/$', views.shop_search_results_page, name='shop_search_results_page'),

    url(r'^box/$', views.safety_deposit_box_page, name='safety_deposit_box_page'),
    url(r'^box/add/$', views.add_box_item, name='add_box_item'),
    url(r'^box/remove/(?P<item>[0-9]+)/$', views.remove_box_item, name='remove_box_item'),
    url(r'^box/upgrade/$', views.upgrade_box, name='upgrade_box'),

    url(r'^trade/$', views.trading_post_page, name='trading_post_page'),
    url(r'^trade/open/$', views.open_trade_page, name='open_trade_page'),
    url(r'^trade/open/processing/$', views.open_trade, name='open_trade'),
    url(r'^trade/personal/$', views.your_trades_page, name='your_trades_page'),
    url(r'^trade/(?P<pk>[0-9]+)/offer/$', views.make_offer_page, name='make_offer_page'),
    url(r'^trade/offer/processing/$', views.make_offer, name='make_offer'),
    url(r'^trade/(?P<original_pk>[0-9]+)/offer/(?P<offer_pk>[0-9]+)/accept/$', views.accept_offer, name='accept_offer'),
    url(r'^trade/(?P<trade_pk>[0-9]+)/cancel/$', views.cancel_trade, name='cancel_trade'),

]
