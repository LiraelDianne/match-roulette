from __future__ import unicode_literals

from django.db import models
from ..login_reg.models import User

from ..login_reg.models import Gender, User

class Option(models.Model):
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Question(models.Model):
    question = models.CharField(max_length=300)
    option_a = models.ForeignKey(Option, related_name='opta')
    option_b = models.ForeignKey(Option, related_name='optb')
    option_c = models.ForeignKey(Option, related_name='optc')
    option_d = models.ForeignKey(Option, related_name='optd')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserAnswer(models.Model):
    answerer = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Option)
    importance = models.IntegerField()

