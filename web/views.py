from django.shortcuts import render, redirect
from web.models import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from datetime import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
import time
import pytz
import pyrebase

"""
    time_now = datetime.now(timezone.utc)
    millis = int(time.mktime(time_now.timetuple()))
    
    
    user = auth.refresh(user['refreshToken'])

"""


config = {
  "apiKey": "your api key",
  "authDomain": "auth domain",
  "databaseURL": "database url",
  "storageBucket": "storage bucket",
  "projectId": "project id",
  "messagingSenderId": "msg sender id"
}

firebase = pyrebase.initialize_app(config)

mAuth = firebase.auth()
database = firebase.database()


# Create your views here.

def adminLogin(request):
    data = {}
    return render(request, "admin-login.html", data)

def adminSignin(request):
    data = {}

    email = request.POST['email']
    password = request.POST['password']

    try:
        user = mAuth.sign_in_with_email_and_password(email, password)
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        return redirect("/admin-home")

    except:
        data['message'] = "Invalid login attempt. Please check your credentials and try again."
        return render(request, "admin-login.html", data)


def adminHome(request):
    data = {}

    idToken = request.session['uid']
    users = mAuth.get_account_info(idToken)
    users = users['users']
    user_profile = users[0]

    data['email'] = user_profile['email']

    return render(request, "admin-index.html", data)


def adminEvents(request):
    data = {}

    idToken = request.session['uid']
    users = mAuth.get_account_info(idToken)
    users = users['users']
    user_profile = users[0]

    data['email'] = user_profile['email']

    events = database.child("events").shallow().get().val()
    event_keys = []

    for event in events:
        event_keys.append(event)

    event_titles = []
    event_images = []
    event_locations = []
    event_times = []
    event_posteds = []
    event_owners = []

    for event in event_keys:
        event_titles.append(database.child("events").child(event).child("title").get().val())
        event_locations.append(database.child("events").child(event).child("location").get().val())
        event_times.append(database.child("events").child(event).child("time").get().val())
        event_owners.append(database.child("events").child(event).child("userName").get().val())
        event_posteds.append(database.child("events").child(event).child("posted").get().val())
        event_images.append(database.child("events").child(event).child("image").get().val())

    data['events'] = zip(event_keys, event_images, event_titles, event_locations, event_times, event_posteds, event_owners)



    return render(request, "admin-events.html", data)

def adminUsers(request):
    data = {}

    idToken = request.session['uid']
    users = mAuth.get_account_info(idToken)
    users = users['users']
    user_profile = users[0]

    users = database.child("users").shallow().get().val()

    users_keys = []

    for user in users:
        users_keys.append(user)

    users_names = []
    users_emails = []
    users_phones = []
    for key in users_keys:
        users_names.append(database.child("users").child(key).child("name").get().val())
        users_emails.append(database.child("users").child(key).child("email").get().val())
        users_phones.append(database.child("users").child(key).child("phone").get().val())

    print(users)

    data['email'] = user_profile['email']
    data['users'] = zip(users_names, users_emails, users_phones, users_keys)
    return render(request, "admin-users.html", data)

def adminReservations(request):
    data = {}

    idToken = request.session['uid']
    users = mAuth.get_account_info(idToken)
    users = users['users']
    user_profile = users[0]

    data['email'] = user_profile['email']

    events = database.child("events").shallow().get().val()
    event_keys = []
    event_titles = []
    reserv_keys = []
    reserv_names = []
    reserv_emails = []
    reserv_refs = []

    for event in events:
        event_keys.append(event)

    for event in events:
        res_keys = database.child("events").child(event).child("reservations").shallow().get().val()

        for key in res_keys:
            reserv_keys.append(key)


    for reserv_key in reserv_keys:
        print(reserv_key)

    # for event in event_keys:
    #     for key in reserv_keys:
    #         ref = database.child("events").child(event).child("reservations").child(key).child("reference").get().val()
    #         if ref is not None:
    #             print(ref)



    """

    for event in event_keys:
        event_titles.append(database.child("events").child(event).child("title").get().val())
        reservations = database.child("events").child(event).child("reservations").shallow().get().val()

        for res in reservations:
            reserv_keys.append(res)


    # for event in event_keys:

    for event in event_keys:
        for res_key in reserv_keys:
            try:
                reserv_names.append(database.child("events").child(event).child("reservations").child(res_key).child("userName").get().val())
                reserv_emails.append(database.child("events").child(event).child("reservations").child(res_key).child("email").get().val())
                reserv_refs.append(database.child("events").child(event).child("reservations").child(res_key).child("reference").get().val())
                print(database.child("events").child(event).child("reservations").child(res_key).child("reference").get().val())

            except:
                pass
    
    """

    data['events'] = event_titles
    data['reservations'] = zip(reserv_keys, reserv_names, reserv_emails, reserv_refs)

    return render(request, "admin-reservations.html", data)


def adminEvent(request, event_id):
    data = {}

    idToken = request.session['uid']
    users = mAuth.get_account_info(idToken)
    users = users['users']
    user_profile = users[0]
    data['email'] = user_profile['email']


    res_keys = database.child("events").child(event_id).child("reservations").shallow().get().val()
    comm_keys = database.child("events").child(event_id).child("comments").shallow().get().val()
    reserv_keys = []
    reserv_names = []
    reserv_emails = []
    reserv_refs = []

    comment_keys = []
    comment_names = []
    comment_comms = []


    for key in res_keys or []:
        reserv_keys.append(key)
        reserv_names.append(
            database.child("events").child(event_id).child("reservations").child(key).child("userName").get().val())
        reserv_emails.append(
            database.child("events").child(event_id).child("reservations").child(key).child("email").get().val())
        reserv_refs.append(database.child("events").child(event_id).child("reservations").child(key).child(
            "reference").get().val())


    for key in comm_keys or []:
        comment_keys.append(key)
        comment_names.append(database.child("events").child(event_id).child("comments").child(key).child("userName").get().val())
        comment_comms.append(database.child("events").child(event_id).child("comments").child(key).child("comment").get().val())



    data['eventTitle'] = database.child("events").child(event_id).child("title").get().val()
    data['eventImage'] = database.child("events").child(event_id).child("image").get().val()
    data['eventDescription'] = database.child("events").child(event_id).child("description").get().val()
    data['eventTime'] = database.child("events").child(event_id).child("time").get().val()
    data['eventLocation'] = database.child("events").child(event_id).child("location").get().val()
    data['eventLatitude'] = database.child("events").child(event_id).child("coordinates").child("latitude").get().val()
    data['eventLongitude'] = database.child("events").child(event_id).child("coordinates").child("longitude").get().val()
    data['reservations'] = zip(reserv_names, reserv_emails, reserv_refs)
    data['comments'] = zip(comment_names, comment_comms)

    return render(request, "admin-event.html", data)


def logout(request):
    auth.logout(request)
    return redirect("/admin-login")




"""GUEST FUNCTIONS"""


def index(request):
    return render(request, "index.html")


def events(request):
    data = {}

    eve_ids = database.child("events").shallow().get().val()

    event_images = []
    event_titles = []
    event_locations = []
    event_times = []
    event_ids = []

    for evId in eve_ids:
        event_ids.append(evId)
        event_images.append(database.child("events").child(evId).child("image").get().val())
        event_titles.append(database.child("events").child(evId).child("title").get().val())
        event_locations.append(database.child("events").child(evId).child("location").get().val())
        event_times.append(database.child("events").child(evId).child("time").get().val())

    data['events'] = zip(event_ids, event_images, event_titles, event_locations, event_times)
    return render(request, "events.html", data)

def event(request, event_id):
    data = {}

    eventUserId = database.child("events").child(event_id).child("user").get().val()

    data['eventTitle'] = database.child("events").child(event_id).child("title").get().val()
    data['eventDescription'] = database.child("events").child(event_id).child("description").get().val()
    data['eventImage'] = database.child("events").child(event_id).child("image").get().val()
    data['eventLocation'] = database.child("events").child(event_id).child("location").get().val()
    data['eventTime'] = database.child("events").child(event_id).child("time").get().val()
    data['eventPostedOn'] = database.child("events").child(event_id).child("postedOn").get().val()
    data['eventOwner'] = database.child("events").child(event_id).child("userName").get().val()
    data['eventLatitude'] = database.child("events").child(event_id).child("coordinates").child("latitude").get().val()
    data['eventLongitude'] = database.child("events").child(event_id).child("coordinates").child("longitude").get().val()
    data['eventOwnerEmail'] = database.child("users").child(eventUserId).child("email").get().val()
    return render(request, "event.html", data)