from __future__ import unicode_literals
import bcrypt
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')



class Gender(models.Model):
    name = models.CharField(max_length=50)


class UserManager(models.Manager):
    def login(self, email, password):
        try:
            user = self.get(email__iexact=email) # case insensitive comparison
            if user and bcrypt.hashpw(password.encode('utf-8'),user.password.encode('utf-8')) == user.password:
                return (True, user)
            return(False,{"login" : "login failed"})
        except:
            return(False,{"login" : "login failed"})

    def register(self, first_name, last_name, alias, email, password, confirm_password, birthday):
        errors = {}
        if first_name == "" or last_name == "" or alias == "" or email == "" or password == "" or confirm_password == "":
            errors['blank'] = "Please fill-in all fields"
        if len(first_name) < 2:
            errors['first_name'] = "First Name is too short"
        if len(last_name) < 2:
            errors['last_name'] = "Last Name is too short"
        if len(alias) < 2:
            errors['alias'] = "Alias is too short"
        if len(password) < 3:
            errors['password'] = "Password is too short"
        if password != confirm_password:
            errors['confirm_password'] = "Passwords must match"
        try:
            user = self.get(email__iexact=email)
            errors['invalid'] = "This email is already in use! (probably not a great thing to tell hackers)"
        except:
            pass

        if not EMAIL_REGEX.match(email):
            errors['email'] = "Please enter a valid email"
        if errors:
            return (False, errors)
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.create(first_name=first_name, last_name=last_name, alias=alias, password=password, email=email, birthday=birthday)
        errors = {"blank" : "", "email" : "", "first_name" : "", "last_name" : "", "alias" : "", "password" : "", "confirm_password" : "", "invalid" : ""}
        return (True, self.get(email=email))

    def update(self, **kwargs):
        first_name = kwargs['first_name']
        last_name = kwargs['last_name']
        alias = kwargs['alias']
        password = kwargs['password']
        confirm_password = kwargs['confirm_password']
        email = kwargs['email']
        gender = kwargs['gender']
        orientation = kwargs['orientation'] #what data type does a checkbox return? Some kind of list?
        description = kwargs['description']
        #logic for email, password, etc like registration
        errors = {}
        if first_name == "" or last_name == "" or alias == "" or email == "" or password == "" or confirm_password == "":
            errors['blank'] = "Please fill-in name, alias, email, and password fields"
        if len(first_name) < 2:
            errors['first_name'] = "First Name is too short"
        if len(last_name) < 2:
            errors['last_name'] = "Last Name is too short"
        if len(alias) < 2:
            errors['alias'] = "Alias is too short"
        if len(password) < 3:
            errors['password'] = "Password is too short"
        if password != confirm_password:
            errors['confirm_password'] = "Passwords must match"
        try:
            user = self.get(email__iexact=email)
            errors['invalid'] = "This email is already in use! (probably not a great thing to tell hackers)"
        except:
            pass

        if not EMAIL_REGEX.match(email):
            errors['email'] = "Please enter a valid email"
        #awkward because it re-salts the password every time - todo: put in different form?
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        #check if a gender is selected
        if not gender:
            errors['gender'] = "Please select a gender"
        #todo: check if at least one orientation box has been checked

        if errors:
            return (False, errors)

        errors = {
            "blank" : "",
            "email" : "",
            "first_name" : "",
            "last_name" : "",
            "alias" : "",
            "password" : "",
            "confirm_password" : "",
            "invalid" : "",
            "gender": "",
            "orientation": "",
            }
        #todo: finish updating user
        user = self.get(email=email)
        user.update()
        return (True, self.get(email=email))

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.EmailField() # auto validation for us!
    password = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userManager = UserManager()
    objects = models.Manager()

    gender = models.ForeignKey(Gender, default='1')
    orientation = models.ManyToManyField(Gender, related_name='talks_to')
    description = models.CharField(max_length=500, default="")
    favorite = models.ManyToManyField('self', related_name='Favorites')
    blocked = models.ManyToManyField('self', related_name='Blocked')


