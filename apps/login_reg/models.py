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

	def register(self, first_name, last_name, alias, email, password, confirm_password):
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
		self.create(first_name=first_name, last_name=last_name, alias=alias, password=password, email=email)
		errors = {"blank" : "", "email" : "", "first_name" : "", "last_name" : "", "alias" : "", "password" : "", "confirm_password" : "", "invalid" : ""}
		return (True, self.get(email=email))

	def update(self, **kwargs):
		errors = {}
		userID = kwargs['userID'][0]
		first_name = kwargs['first_name'][0]
		last_name = kwargs['last_name'][0]
		alias = kwargs['alias'][0]
		gender = kwargs['gender'][0]
		if 'orientation[]' not in kwargs:
			errors['orientation'] = "Please tell us who you're interested in!"
		else:
			orientation = kwargs['orientation[]']
		description = kwargs['description'][0]

		if first_name == "" or last_name == "" or alias == "":
			errors['blank'] = "Please fill-in name, alias fields"
		if len(first_name) < 2:
			errors['first_name'] = "First Name is too short"
		if len(last_name) < 2:
				errors['last_name'] = "Last Name is too short"
		if len(alias) < 2:
				errors['alias'] = "Alias is too short"
		#check if a gender is selected
		if gender == "1":
				errors['gender'] = "Please select a gender"
		if errors:
			return (False, errors)

		errors = {
			"blank" : "",
			"first_name" : "",
			"last_name" : "",
			"alias" : "",
			"gender": "",
			"orientation": "",
			}
		user = User.objects.get(id = userID)
		User.objects.filter(id=userID).update(first_name=first_name, last_name=last_name, alias=alias, gender=gender, description = description)
		for gender_id in orientation:
			gender = Gender.objects.get(id=gender_id)
			user.orientation.add(gender)
		return (True, self.get(id=userID))

class User(models.Model):
		first_name = models.CharField(max_length=45)
		last_name = models.CharField(max_length=45)
		alias = models.CharField(max_length=45)
		email = models.EmailField() # auto validation for us!
		password = models.CharField(max_length=255)
		created_at = models.DateTimeField(auto_now_add=True)
		updated_at = models.DateTimeField(auto_now=True)
		userManager = UserManager()
		objects = models.Manager()

		gender = models.ForeignKey(Gender, default='1')
		orientation = models.ManyToManyField(Gender, related_name='talks_to')
		description = models.CharField(max_length=500, default="")
		favorite = models.ManyToManyField('self', related_name='Favorites')
		blocked = models.ManyToManyField('self', related_name='Blocked')
