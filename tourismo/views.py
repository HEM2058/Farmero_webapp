from django.shortcuts import render, redirect ,HttpResponse
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import datetime
import requests
import json
# Create your views here.

def Base(request):
    return render(request,"base.html")

# user pages
def Index1(request):
    return render(request,"index1.html")
def Index2(request):
    return render(request,"index2.html")

def Index3(request):
    coordinates = request.GET.get('coordinates')
    print(coordinates)
    plan = Plan.objects.all()
    
    if coordinates:
        return render(request, 'index3.html',{'plan':plan,'coordinates':coordinates})
    return render(request,'index3.html',{'plan':plan})
def Help(request):
    return render(request,"help.html")
def Payment(request):
    return render(request,'Guide/payment.html')
# tourist user
def TSignUp(request):
  return render(request,"Tourist/signup.html")
def TSignInPage(request):
  return render(request,"Tourist/login.html")

def TRegistration(request):
    if (request.method=="POST"):

        uname = request.POST["uname"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        country = request.POST["country"]
        sex = request.POST["sex"]
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        Tuser = Tourist.objects.filter(email=email)  
        if(Tuser):
            msg = "FarmMart with this email address is already exist!"
            return render(request,'Tourist/signup.html',{'msg':msg})      
        else:
            if(password==cpassword):
                 Tuser = Tourist.objects.create(uname=uname,email=email,contact=contact, country= country,sex=sex, password=password)
                 return render(request,'Tourist/login.html',{'email':email})

            else:
                msg = "Password and Confirm password does not match !"
                return render(request,'Tourist/signup.html',{'msg':msg})
            
def TSignIn(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            Tuser = Tourist.objects.get(email=email)
        except ObjectDoesNotExist:
            msg = "User with this email address does not exist"
            return render(request, 'Tourist/login.html', {'msg': msg})

        if Tuser.password == password:
            request.session['id'] = Tuser.id
            msg = f"Welcome {Tuser.uname}! You have successfully logged in as FarmMart"
            return render(request, 'index2.html', {'msg': msg})
        else:
            msg = "Please enter a valid password"
            return render(request, 'Tourist/login.html', {'msg': msg})


# Guide user
def GSignUp(request):
  return render(request,"Guide/signup.html")
def GSignInPage(request):
  return render(request,"Guide/login.html")

def GRegistration(request):
    if (request.method=="POST"):

        uname = request.POST["uname"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        country = request.POST["country"]
        sex = request.POST["sex"]
        lat = request.POST["lat"]
        lng = request.POST["lng"]
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        Guser = Guide.objects.filter(email=email)  
        if(Guser):
            msg = "AgroBuyer with this email address is already exist!"
            return render(request,'Guide/signup.html',{'msg':msg})      
        else:
            if(password==cpassword):
                 
                 Guser = Guide.objects.create(uname=uname,email=email,contact=contact, country= country,lat=lat, lng=lng, sex=sex, password=password)
                 return render(request,'Guide/login.html',{'email':email})

            else:
                msg = "Password and Confirm password does not match !"
                return render(request,'Guide/signup.html',{'msg':msg})
            
            
def GSignIn(request):
    if (request.method=="POST"):
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            Guser = Guide.objects.get(email=email)
        except ObjectDoesNotExist:
            msg = "User with this email address does not exist"
            return render(request, 'Guide/login.html', {'msg': msg})

        if (Guser.password == password):
            request.session['id'] = Guser.id
            request.session['uname'] = Guser.uname
            plan = Plan.objects.all()
            msg = f"Welcome {Guser.uname}! You have successfully logged in as AgroBuyer"
            return render(request, 'index3.html', {'msg': msg, 'plan':plan})
        else:
            msg = "Please enter valid password"
            return render(request, 'Guide/login.html', {'msg': msg})  
        

# Creating plan by tourists



def create_plan(request,pk):
    if request.method == 'POST':
        tourist = Tourist.objects.get(pk=pk)
        pcoordinate = request.POST['pcoordinate']
        product = request.POST.get('product')
        quantity = request.POST['quantity']
        budget = request.POST['budget']


      
        
        # create new Plan object
        plan = Plan.objects.create(
            tourist=tourist,
            pcoordinate=pcoordinate,
            product=product,
            quantity=quantity,
            budget=budget
        )
        
        # msg = "Plan has been successfully posted !"
        return redirect('yourplans',pk=pk)
  
    return render(request, "index2.html")


#Guide application request


# def add_guide(request, plan_id, guide_id):
#     plan = Plan.objects.get(id=plan_id)
#     guide = Guide.objects.get(id=guide_id)
  
#     guide_request, created = GuideRequest.objects.get_or_create(plan=plan, guide=guide)
#     session_id = request.session.get('id')
#     if created:
       
#           return redirect('appliedplans', pk=session_id)
#     else:
#           return redirect('appliedplans', pk=session_id)
    
def add_guide(request, plan_id, guide_id):
    plan = Plan.objects.get(id=plan_id)
    guide = Guide.objects.get(id=guide_id)
    tourist_id = plan.tourist.id
    quantity_order = request.POST['quantity_order']
    guide_request, created = GuideRequest.objects.get_or_create(plan=plan, guide=guide,quantity_order= quantity_order)
    session_id = request.session.get('id')
    if created:
        expire_at = timezone.now() + datetime.timedelta(days=1)  # set TTL to 1 day
        message = f"The {guide.uname} AgroBuyer has requested to buy {quantity_order}kg {plan.product}."
        TouristNotification.objects.create(tourist=tourist_id,message=message,expire_at=expire_at)
        # Get the channel layer for sending WebSocket messages
        channel_layer = get_channel_layer()
        
        # Get the WebSocket group name for the tourist
        group_name = f'tourist_{plan.tourist.id}'
        
        # Send a WebSocket message to the tourist group
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'guide_request_created',
                'plan_id': plan.id,
                'guide_id': guide.id,
                'guide_uname' : guide.uname,
                'quantity_order' :quantity_order,
                'product' : plan.product,
            }
        )
       
        return redirect('appliedplans', pk=session_id)
    else:
        return redirect('appliedplans', pk=session_id)









def YourPlans(request,pk):
    tourist = Tourist.objects.get(id=pk)
    if request.session.get('id') != pk:
        return HttpResponse('<h1>You are not authorized to view this page !</h1>')
    else:
        plans = Plan.objects.filter(tourist=tourist)
        return render(request,'Tourist/plans.html',{'plan':plans})



def accept_guide_request(request,guide_id,plan_id):
    guide = Guide.objects.get(id=guide_id)
    plan = Plan.objects.get(id=plan_id)
    guide_request = GuideRequest.objects.get(guide=guide,plan=plan)
    guide_request.accepted = True
    guide_request.save()
    session_id = request.session.get('id')
    # msg = f"You have accepted the request made by {guide.uname}! Please rate the {guide.uname} after your tour."
    return redirect('yourplans', pk=session_id)


def AppliedPlans(request,pk):
    guide = Guide.objects.get(id=pk)
    guiderequest = GuideRequest.objects.filter(guide=guide)
    if request.session.get('id')!=pk:
          return HttpResponse('<h1>You are not authorized to view this page !</h1>')
    else:
          return render(request,'Guide/plans.html',{ 'guiderequest':guiderequest})
    


def get_guide_info_ajax(request, guide_id):
    guide = Guide.objects.get(id=guide_id)
    guide_info = {
        'guide_id':guide_id,
        'uname': guide.uname,
        'contact': guide.contact,
        'email': guide.email,
         'sex'  :guide.sex,
    }
    return JsonResponse(guide_info)





#24 hours notification showing in tourist page 


def get_Tnotifications(request):
    if request.session.get('id') is not None:  # check if tourist is logged in
        tourist_id = request.session['id']
        notifications = TouristNotification.objects.filter(tourist=tourist_id).order_by('-created_at')
        data = []
        for notification in notifications:
            data.append({
                'message': notification.message,
                'created_at': timezone.localtime(notification.created_at).strftime('%Y-%m-%d %H:%M:%S'),
                'expire_at': timezone.localtime(notification.expire_at).strftime('%Y-%m-%d %H:%M:%S'),
            })
        return JsonResponse({'notifications': data})
    else:
        return JsonResponse({'error': 'Tourist not logged in'})
    


#Drive reauest to guide from tourist

def create_guide_request(request, guide_id):
    if request.method == 'POST':
        guide = Guide.objects.get(id=guide_id)
        tourist_id = request.session.get('id')
        tourist = Tourist.objects.get(id=tourist_id)
        tourist_request, created =  TouristRequest.objects.get_or_create(tourist=tourist,guide=guide)
        if created:
             expire_at = timezone.now() + datetime.timedelta(days=1)  # set TTL to 1 day
             message = f"The {tourist.uname} FarmMart wanted to sell an agricultral product.You can contact them at {tourist.contact}."
             GuideNotification.objects.create(guide=guide.id,message=message,expire_at=expire_at)
              # Get the channel layer for sending WebSocket messages
             channel_layer = get_channel_layer()
        
              # Get the WebSocket group name for the tourist
             group_name = f'guide_{guide.id}'
        
              # Send a WebSocket message to the tourist group
             async_to_sync(channel_layer.group_send)(
              group_name,
              {
                'type': 'tourist_request_created',
                'guide_id': guide.id,
                'tourist_uname' : tourist.uname,
                'tourist_contact':tourist.contact,
            }
        )
             return JsonResponse({'status': 'success'})
        else:
                # Get the channel layer for sending WebSocket messages
             channel_layer = get_channel_layer()
        
              # Get the WebSocket group name for the tourist
             group_name = f'guide_{guide.id}'
        
              # Send a WebSocket message to the tourist group
             async_to_sync(channel_layer.group_send)(
              group_name,
              {
                'type': 'tourist_request_created',
                'guide_id': guide.id,
                'tourist_uname' : tourist.uname,
                 'tourist_contact':tourist.contact,
            }
        )
             return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    


def get_Gnotifications(request):
    if request.session.get('id') is not None:  # check if tourist is logged in
        guide_id = request.session['id']
        notifications = GuideNotification.objects.filter(guide=guide_id).order_by('-created_at')
        data = []
        for notification in notifications:
            data.append({
                'message': notification.message,
                'created_at': timezone.localtime(notification.expire_at).strftime('%Y-%m-%d %H:%M:%S'),
                'expire_at': timezone.localtime(notification.expire_at).strftime('%Y-%m-%d %H:%M:%S'),
            })
        return JsonResponse({'notifications': data})
    else:
        return JsonResponse({'error': 'Tourist not logged in'})  
    




#Hotel informatio
def addHotel(request):
    return render(request,'Guide/hotel.html')
def Hindex(request):
    return render(request,"Tourist/hotel/index.html")

def Hcontact(request):
    return render(request,"Tourist/hotel/contact.html")
   
def RoomDetail(request):
    return render(request,"Tourist/hotel/room-details.html")


def create_hotel(request):
    if request.method == 'POST':
        # Get the form input values from the request
        name = request.POST.get('hotel-name')
        video_intro = request.FILES.get('video-intro')
        room_size = request.POST.get('room-size')
        room_prices_per_night = request.POST.get('room-prices')
        room_details = request.POST.get('room-details')
        room_images = request.FILES.getlist('room-images')
        tour_package_images = request.FILES.getlist('tour-package-images')
        food_and_drink_images = request.FILES.getlist('food-drink-images')

        # Create a new Hotel instance
        hotel = Hotel(
            name=name,
            video_intro=video_intro,
            room_size=room_size,
            room_prices_per_night=room_prices_per_night,
            room_details=room_details
        )

        # Save the hotel object to the database
        hotel.save()

        # Save room images
        for image in room_images:
            hotel.room_images.create(image=image)

        # Save tour package images
        for image in tour_package_images:
            hotel.tour_package_images.create(image=image)

        # Save food and drink images
        for image in food_and_drink_images:
            hotel.food_and_drink_images.create(image=image)

        # Redirect to a success page or perform any other desired action
        return redirect('index3')

    return render(request, 'Guide/hotel.html')



#OSM overpass api to filter data


#for hotel



def retrieve_hotel_data(bbox):
    print("+++++++++++++++++++++======================================================================================")
    print(bbox)
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = """
    [out:json][timeout:25];
    // gather results
    (
     // query part for: “tourism=hotel”
  node["tourism"="hotel"]({{bbox}});
  way["tourism"="hotel"]({{bbox}});
  relation["tourism"="hotel"]({{bbox}});
    );
    // print results
    out body;
>;
out skel qt;
    """

    formatted_query = query.replace("{{bbox}}", bbox)
    print(formatted_query)
    response = requests.get(overpass_url, params={"data": formatted_query})
    print("=======================================")
    print(response)
    if response.status_code == 200:
        print("Inside if statement")
        data = response.json()
        print("===================data======================")
        print(data)
        hotel = data["elements"]
        # Print the number of hotels
        print("Number of hotels:", len(hotel))
        return hotel
    else:
        return []

def hotel_list(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Process the AJAX request and retrieve the bounding box data
        bbox = request.POST.get('bbox')
        print("======================================================================================")
        print(bbox)
        # Retrieve hotel data using the Overpass API
        hotels = retrieve_hotel_data(bbox)

        return JsonResponse(hotels, safe=False)

    return JsonResponse({'error': 'Invalid request.'})


#for atms

def retrieve_atm_data(bbox):
    print("+++++++++++++++++++++======================================================================================")
    print(bbox)
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = """
    [out:json][timeout:25];
    // gather results
    (
     // query part for: “amenity=atm”
   node["shop"="agrarian"]({{bbox}});
  way["shop"="agrarian"]({{bbox}});
  relation["shop"="agrarian"]({{bbox}});
    );
    // print results
    out body;
>;
out skel qt;
    """

    formatted_query = query.replace("{{bbox}}", bbox)
    print(formatted_query)
    response = requests.get(overpass_url, params={"data": formatted_query})
    print("=======================================")
    print(response)
    if response.status_code == 200:
        print("Inside if statement")
        data = response.json()
        print("===================data======================")
        print(data)
        atms = data["elements"]
        # Print the number of hotels
        print("Number of hotels:", len(atms))
        return atms
    else:
        return []

def atm_list(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Process the AJAX request and retrieve the bounding box data
        bbox = request.POST.get('bbox')
        print("======================================================================================")
        print(bbox)
        # Retrieve hotel data using the Overpass API
        hotels = retrieve_atm_data(bbox)

        return JsonResponse(hotels, safe=False)

    return JsonResponse({'error': 'Invalid request.'})
