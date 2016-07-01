from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.utils.crypto import get_random_string

from ..login_reg.models import Gender, User, UserManager
from .models import Question, UserAnswer
from .matching import findMatch

import copy
from datetime import datetime

import threading
import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s',)


def home(request):
    context = {
        'user': User.objects.get(id=request.session['id']),
        'people' : User.objects.all()
    }
    return render(request, "dating_app/main.html", context)

def profilePage(request, id):
    #this page loads the profile information and then compiles the resulting page...
    #Todo!  It determines if the user should be shown their own (editable) page or a static page of another users
    #Crystal: can this just be an edit button in the template that only displays if the user id is the same as the session id?
    currentuser=User.objects.get(id=request.session['id'])
    context = {
        'user': currentuser,
        'genders': Gender.objects.all(),

    }
    #todo: get errors working
    return render(request, "dating_app/profile.html", context)


def update_profile(request):
    #submit form from profile page
    if request.method == "POST":
        user = User.userManager.update(**request.POST)
        if user[0]:
            request.session['errors']
            return redirect(reverse("da_home"))
        else:
            request.session['errors'] = user[1]
        #return to home page, or updated profile page?
        return redirect(reverse("da_profile"))

def loggedIn(request):
    if 'id' in request.session:
        return redirect(reverse("da_home"))
    else:
        return redirect(reverse("rl_index"))

def questionnaire_page(request, id):
    context = {
     'user': User.objects.get(id=request.session['id']),
     'questions': Question.objects.all()
    }
    return render (request, "dating_app/questions.html", context)

def submit_questionnaire(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session.id)
        for i in range(1, 6):
            question = Question.objects.get(id=i)
            UserAnswer.objects.create(answerer=user, question=question,
                answer=request.session[str(i)],
                importance=request.session['importance'])
        return redirect(reverse("da_home"))

    return redirect(reverse("da_question"))

def find_match(request):
    user = User.objects.get(id=request.session['id'])
    sessions = Session.objects.all()
    queue = []
    for session in sessions:
        key = session.session_key
        s = SessionStore(session_key=key)
        if s['status'] == "active":
            queue.append(s)
    # now I have a queue which is a list of active sessions
    timesortedqueue = sorted(queue, key=itemgetter('queued'))
    print timesortedqueue
    # sorted by oldest first
    match = findMatch(user, timesortedqueue)
    # check for users
    if match:
    # if match found:
        match['match'] = "found"
        request.session['match'] = "found"
        match.save()
        #save the match session
        return render(request, "dating_app/found.html")

    else:
        #mark them as active so they get sorted into the queue
        request.session['status'] = "active"
        #give them a timestamp
        request.session['queued'] = datetime.now()
        return redirect(reverse('da_waiting'))

def Timeout():
    timeout = True

def checkmatch(request):
    #kick them out after five minutes
    timeout = False
    timer = threading.Timer(60*5, Timeout)
    timer.start()

    while not timeout:
        if request.session['match'] == "found":
            return render(request, "dating_app/found.html")
    request.session['status'] = ""
    request.session['match'] = "not found"

    return render(request, "dating_app/main.html")


def wait(request):
    queue = threading.Thread(target=checkmatch, args=(request, ))

    return render(request, 'dating_app/wait.html')


def foundmatch(request):
    return render(request, 'dating_app/found.html')

def end_match(request):
    request.session['match'] = ""
    return redirect(reverse("da_home"))
