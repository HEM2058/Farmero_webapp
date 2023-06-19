from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
# Create your models here.


class Tourist(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    uname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    sex = models.CharField(max_length=50)
   
    def __str__(self):
        return self.uname
    

class Guide(models.Model):
    #  user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
     uname = models.CharField(max_length=50)
     email = models.EmailField(max_length=254)
     password = models.CharField(max_length=50)
     country = models.CharField(max_length=50)
     contact = models.CharField(max_length=50)
     sex = models.CharField(max_length=50)
     lat = models.FloatField()
     lng = models.FloatField()
     latitude = models.FloatField(null=True)
     longitude = models.FloatField(null=True)
     def __str__(self):
         return self.uname


class Plan(models.Model):
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    guides = models.ManyToManyField(Guide, related_name='plans')
    guide_requests = models.ManyToManyField(Guide, through='GuideRequest', related_name='plan_requests')
    pcoordinate = models.CharField(max_length=50,null=True)
    product = models.CharField(max_length=150,null=True)
    quantity = models.IntegerField(null=True)
    budget = models.IntegerField(null=True)
    remaining_quantity = models.IntegerField(null=True)
    
    def save(self, *args, **kwargs):
        if self.remaining_quantity is None:
            self.remaining_quantity = self.quantity
        super().save(*args, **kwargs)

    def update_remaining_quantity(self):
        guide_requests = self.guiderequest_set.filter()
        total_ordered_quantity = guide_requests.aggregate(total=Sum('quantity_order'))['total']
        if total_ordered_quantity is not None:
            self.remaining_quantity = self.quantity - total_ordered_quantity
        else:
            self.remaining_quantity = self.quantity
        self.save()
    
    
   



class GuideRequest(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    date_requested = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    quantity_order = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.plan.update_remaining_quantity()

    
    
class TouristNotification(models.Model):
    tourist = models.IntegerField(null=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    expire_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expire_at

class TouristRequest(models.Model):
       tourist = models.ForeignKey(Tourist,on_delete=models.CASCADE)
       guide = models.ForeignKey(Guide,on_delete=models.CASCADE,null=True)
       date_requested = models.DateTimeField(auto_now_add=True)
      

   
class GuideNotification(models.Model):
    guide = models.IntegerField(null=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    expire_at = models.DateTimeField()


#Hotel model

class RoomImage(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='room_images')
    image = models.ImageField(upload_to='room_images/', max_length=100)

class TourPackageImage(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='tour_package_images')
    image = models.ImageField(upload_to='tour_package_images/', max_length=100)

class FoodAndDrinkImage(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='food_and_drink_images')
    image = models.ImageField(upload_to='food_and_drink_images/', max_length=100)



class Hotel(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    video_intro = models.FileField(upload_to='hotel_videos/', max_length=100, null=True)
    room_size = models.CharField(max_length=100)
    room_prices_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    room_details = models.TextField()