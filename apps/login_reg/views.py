from django.shortcuts import render, HttpResponse, redirect
from .models import User, UserManager, Gender
from django.core.urlresolvers import reverse
import copy

def index(request):
    try:
        request.session['error']
    except:
        request.session['errorLogin'] = {"login" : ""}
        request.session['error'] = {"blank" : "", "email" : "", "first_name" : "", "last_name" : "", "alias" : "", "password" : "", "confirm_password" : "", "invalid" : ""}
    return render(request, "login_reg/index.html", {"errors" : request.session['error'], "errorsLogin" : request.session['errorLogin']})

def login(request):
    if request.method == 'POST':
        user_tuple = User.userManager.login(request.POST['email'], request.POST['password'])
        if user_tuple[0]: # true or false from the returned tuple
            request.session['id'] = user_tuple[1].id
            request.session['name'] = user_tuple[1].first_name
            request.session['alias'] = user_tuple[1].alias
            request.session['email'] = user_tuple[1].email
            request.session['error'] = {"blank" : "", "email" : "", "first_name" : "", "last_name" : "", "alias" : "", "password" : "", "confirm_password" : "", "invalid" : ""}
            return redirect(reverse('da_home'))
        else:
            request.session['errorLogin'] = user_tuple[1]
            request.session['error'] = {"blank" : "", "email" : "", "first_name" : "", "last_name" : "", "alias" : "", "password" : "", "confirm_password" : "", "invalid" : ""}
            return redirect (reverse('rl_index'))

def register(request):
    if request.method == 'POST':
        user_tuple = User.userManager.register(request.POST['first_name'], request.POST['last_name'], request.POST['alias'], request.POST['email'], request.POST['password'], request.POST['confirm_password'])
        if user_tuple[0]:
            request.session['id'] = user_tuple[1].id
            request.session['email'] = user_tuple[1].email
            request.session['name'] = user_tuple[1].first_name
            request.session['alias'] = user_tuple[1].alias
            request.session['error'] = {"blank" : "", "email" : "", "first_name" : "", "last_name" : "", "alias" : "", "password" : "", "confirm_password" : "", "invalid" : ""}
            return redirect(reverse('da_profile', kwargs={'id':user_tuple[1].id}))
        else:
            request.session['errorLogin'] = {"login" : ""}
            request.session['error'] = user_tuple[1]
            return redirect (reverse('rl_index'))

def reset(request):
    request.session.clear()
    return redirect (reverse('rl_index'))
