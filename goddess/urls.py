from django.urls import re_path
from . import views

urlpatterns = [
    re_path(
        r"^goddess/neglect/$", views.goddess_neglect_page, name="goddess_neglect_page"
    ),
    re_path(
        r"^goddess/neglect/collect/$",
        views.goddess_neglect_collect,
        name="goddess_neglect_collect",
    ),
    re_path(
        r"^goddess/garden/$", views.goddess_garden_page, name="goddess_garden_page"
    ),
    re_path(r"^goddess/ocean/$", views.goddess_ocean_page, name="goddess_ocean_page"),
    re_path(
        r"^goddess/commerce/$",
        views.goddess_commerce_page,
        name="goddess_commerce_page",
    ),
    re_path(r"^goddess/sun/$", views.goddess_sun_page, name="goddess_sun_page"),
    re_path(
        r"^goddess/(?P<goddess>[A-Za-z]+)/quest/$",
        views.start_goddess_quest,
        name="start_goddess_quest",
    ),
    re_path(
        r"^goddess/(?P<goddess>[A-Za-z]+)/quest/complete/$",
        views.complete_goddess_quest,
        name="complete_goddess_quest",
    ),
    re_path(
        r"^goddess/(?P<goddess>[A-Za-z]+)/quest/cancel/$",
        views.cancel_goddess_quest,
        name="cancel_goddess_quest",
    ),
]
