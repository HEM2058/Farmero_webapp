
from django.urls import path
from tourismo import views
urlpatterns = [
    path('',views.Base,name="base"),

    #user pages
    path('Normal_User/',views.Index1,name="index1"),
    path('Tourist_User/',views.Index2,name="index2"),
    path('Guide_User/',views.Index3,name="index3"),
    path('help/',views.Help,name="help"),
    path('payment/',views.Payment,name="payment"),
    #tourist user
    path('TouristSignup/',views.TSignUp,name="tsignup"),
    path('TouristSignIn/',views.TSignInPage,name="tsignin"),
    path('CreatingTourist/',views.TRegistration,name="tregistration"),
    path('loginTourist/',views.TSignIn,name="tvalidate"),
     #Guide user
    path('GuideSignup/',views.GSignUp,name="gsignup"),
    path('GuideSignIn/',views.GSignInPage,name="gsignin"),
    path('CreatingGuide/',views.GRegistration,name="gregistration"),
    path('loginGuide/',views.GSignIn,name="gvalidate"),

    #posting the plan by tourists
    path('create_plan/<int:pk>',views.create_plan,name="create_plan"),

    #Application for plan by guide
    path('Application/<int:plan_id>/add_guide/<int:guide_id>/',views.add_guide, name='add_guide'),

    #TouristPlans

    path('yourplans/<int:pk>',views.YourPlans,name="yourplans"),

    #Accepting guide request
    path('guide_request/<int:guide_id>/plan_expired/<int:plan_id>', views.accept_guide_request, name='accept_guide_request'),

    #Applied plans rendering at guide page

    path('appliedplans/<int:pk>',views.AppliedPlans,name="appliedplans"),

    # Ajax for reveal guide information
    path('get_guide_info/<int:guide_id>/', views.get_guide_info_ajax, name='get_guide_info_ajax'),

    #Getting application notiication at tourist page
    path('get_tourist_notifications/', views.get_Tnotifications, name='get_tourist_notifications'),

    #Drive reauest to the guide
    path('create_guide_request/<int:guide_id>/', views.create_guide_request, name='create_guide_request'),

    #Getting request notiication at guide page
    path('get_guide_notifications/', views.get_Gnotifications, name='get_guide_notifications'),

    #Hotel information
    path('addhotel/',views.addHotel,name='addhotel'),
    path('hindex/',views.Hindex,name='hindex'),
    path('hcontact/',views.Hcontact,name='hcontact'),
    path('hroomdetail/',views.RoomDetail,name='roomdetail'),
    path('savehotel/',views.create_hotel,name='savehotel'),


    #OSM filter using overpass api
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('atms/', views.atm_list, name='atm_list'),

]
from django.conf.urls.static import static
from django.conf import settings

# ... Your other code ...

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
