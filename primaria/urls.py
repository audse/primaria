from django.urls import include, re_path
from django.contrib import admin

urlpatterns = [
    re_path(r"^secrets/", admin.site.urls),
    re_path(r"", include("core.urls")),
    re_path(r"", include("shop.urls")),
    re_path(r"", include("world.urls")),
    re_path(r"", include("social.urls")),
    re_path(r"", include("goddess.urls")),
]
