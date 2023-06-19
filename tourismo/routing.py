# routing.py

from django.urls import re_path
from . import consumers
# from tourismo.consumers import LocationConsumer
from tourismo.consumers import *

websocket_urlpatterns = [
    # re_path(r'ws/location/$', consumers.LocationConsumer.as_asgi()),
    re_path(r'wss/guide/$', consumers.GuideConsumer.as_asgi()),
    re_path(r'wss/tourist/$', consumers.TouristConsumer.as_asgi()),
    re_path(r'wss/touristNotification/(?P<tourist_id>\d+)/$', consumers.TouristConsumerNotification.as_asgi()),
    re_path(r'wss/guideNotification/(?P<guide_id>\d+)/$', consumers.GuideConsumerNotification.as_asgi()),



    
]
