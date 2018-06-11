from django.conf.urls import url
from . import views

urlpatterns = [

    # GUEST URLS

    # index
    url('^$', views.index, name="Home"),

    # Events
    url('^events$', views.events, name = "Events"),

    #Event
    url(r'^events/(?P<event_id>[-\w]+)$', views.event, name = "Event"),









    #ADMIN URLS

    #Index
    url('^admin-login$', views.adminLogin, name = "Admin home"),

    #Index
    url('^admin-signin$', views.adminSignin, name = "Admin home"),

    #Index
    url('^admin-home$', views.adminHome, name = "Admin home"),

    #Users
    url('^admin-users$', views.adminUsers, name = "Admin home"),

    #Events
    url('^admin-events$', views.adminEvents, name = "Admin home"),

    #Event
    url(r'^admin-events/(?P<event_id>[-\w]+)$', views.adminEvent, name = "Admin home"),

    #Reservations
    url('^admin-reservations$', views.adminReservations, name = "Admin home"),

    #Logout
    url('^logout', views.logout, name = "Admin home"),

]
