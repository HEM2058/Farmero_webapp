from channels.generic.websocket import AsyncWebsocketConsumer
import json
from tourismo.models import TouristNotification
from datetime import timedelta
from django.utils import timezone
import datetime
from asgiref.sync import sync_to_async
from .models import Tourist

class GuideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'guides',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'guides',
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        latitude = data['latitude']
        longitude = data['longitude']
        guide_id = data['guide_id']
        guide_uname = data['guide_uname']
        print("======================================================================================================")
        print(latitude)
        # Save the updated location in the database for the guide
        # ...
        
        # Broadcast the updated location to all connected tourist clients
        await self.channel_layer.group_send(
            'tourists',
            {
                'type': 'location.update',
                'latitude': latitude,
                'longitude': longitude,
                'guide_id' : guide_id,
                'guide_uname' : guide_uname

            }
        )


class TouristConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'tourists',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'tourists',
            self.channel_name
        )

    async def location_update(self, event):
        latitude = event['latitude']
        longitude = event['longitude']
        guide_id =  event['guide_id']
        guide_uname = event['guide_uname']
        await self.send(text_data=json.dumps({'latitude': latitude, 'longitude': longitude,'guide_id': guide_id, 'guide_uname': guide_uname}))


#Notification on creating application by guide


class TouristConsumerNotification(AsyncWebsocketConsumer):
    async def connect(self):
        tourist_id = self.scope['url_route']['kwargs']['tourist_id']
        self.group_name = f'tourist_{tourist_id}'
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def guide_request_created(self, event):
        plan_id = event['plan_id']
        guide_id = event['guide_id']
        quantity_order = event['quantity_order']
        guide_uname = event['guide_uname']
        product = event['product']
        tourist_id = self.scope['url_route']['kwargs']['tourist_id']
        message = f"The {guide_uname} AgroBuyer has request to buy {quantity_order}kg {product}  "
        # expire_at = timezone.now() + datetime.timedelta(days=1)  # set TTL to 1 day
        # try:
        #   save_notification = sync_to_async(TouristNotification.objects.create)
        #   notification = await save_notification(tourist=tourist_id,message=message, expire_at=expire_at)
        # except Exception as e:
        #    print(f"Error saving notification: {e}")
        
        await self.send(text_data=json.dumps({'message': message}))




#Notification on requesting guide by tourist


class GuideConsumerNotification(AsyncWebsocketConsumer):
    async def connect(self):
        guide_id = self.scope['url_route']['kwargs']['guide_id']
        self.group_name = f'guide_{guide_id}'
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def tourist_request_created(self, event):
        tourist_uname = event['tourist_uname']
        tourist_contact = event['tourist_contact']
        message = f"The {tourist_uname} FarmMart has requested to sell the product.You can contact them at {tourist_contact}."
     
        
        await self.send(text_data=json.dumps({'message': message}))