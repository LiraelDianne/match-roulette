from django.shortcuts import render, HttpResponse, redirect
from ..login_reg.models import Gender, User, UserManager
from .models import Question, UserAnswer
from django.core.urlresolvers import reverse
import copy
from datetime import date

def home(request):
    context = {
        'user': User.objects.get(id=request.session['id']),
        'people' : User.objects.all()
    }
    return render(request, "dating_app/main.html", context)

def bobtest(request):
    return render(request, "dating_app/bobtest.html")

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
