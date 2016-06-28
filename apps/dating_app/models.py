from __future__ import unicode_literals

from django.db import models
from ..login_reg.models import User

from ..login_reg.models import Gender, User

class Question(models.Model):
    question = models.CharField(max_length=300)
    option_a = models.CharField(max_length=300)
    option_b = models.CharField(max_length=300)
    option_c = models.CharField(max_length=300)
    option_d = models.CharField(max_length=300)
    image = models.FilePathField(path="/static/images", default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserAnswer(models.Model):
    answerer = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=100)
    importance = models.IntegerField()

