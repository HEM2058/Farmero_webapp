from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Tourist)
admin.site.register(Guide)
admin.site.register(Plan)
admin.site.register(GuideRequest)
admin.site.register(TouristNotification)
admin.site.register(TouristRequest)
admin.site.register(GuideNotification)

#Hotel
admin.site.register(Hotel)
admin.site.register(RoomImage)
admin.site.register(TourPackageImage)
admin.site.register(FoodAndDrinkImage)
