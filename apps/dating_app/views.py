from django.shortcuts import render, HttpResponse, redirect
from ..login_reg.models import Gender, User
from django.core.urlresolvers import reverse
import copy

def home(request):
    context = {
        'user': User.objects.get(id=request.session['id'])
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
    return render(request, "dating_app/profile.html", context)

def update_profile(request):
    #submit form from profile page
    if request.method == "POST":
        user = User.objects.get(id=request.session['id'])
        user.userManager.update(**request.POST)
        #return to home page, or updated profile page?
        return

def loggedIn(request):
    if 'id' in request.session:
        return redirect(reverse("da_home"))
    else:
        return redirect(reverse("rl_index"))
