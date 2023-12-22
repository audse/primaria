from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^goddess/neglect/$", views.goddess_neglect_page, name="goddess_neglect_page"),
    url(
        r"^goddess/neglect/collect/$",
        views.goddess_neglect_collect,
        name="goddess_neglect_collect",
    ),
    url(r"^goddess/garden/$", views.goddess_garden_page, name="goddess_garden_page"),
    url(r"^goddess/ocean/$", views.goddess_ocean_page, name="goddess_ocean_page"),
    url(
        r"^goddess/commerce/$",
        views.goddess_commerce_page,
        name="goddess_commerce_page",
    ),
    url(r"^goddess/sun/$", views.goddess_sun_page, name="goddess_sun_page"),
    url(
        r"^goddess/(?P<goddess>[A-Za-z]+)/quest/$",
        views.start_goddess_quest,
        name="start_goddess_quest",
    ),
    url(
        r"^goddess/(?P<goddess>[A-Za-z]+)/quest/complete/$",
        views.complete_goddess_quest,
        name="complete_goddess_quest",
    ),
    url(
        r"^goddess/(?P<goddess>[A-Za-z]+)/quest/cancel/$",
        views.cancel_goddess_quest,
        name="cancel_goddess_quest",
    ),
]
