from django.contrib import admin
from .models import Score, DailyClaim, MedicinePickup

admin.site.register(Score)
admin.site.register(DailyClaim)
admin.site.register(MedicinePickup)
