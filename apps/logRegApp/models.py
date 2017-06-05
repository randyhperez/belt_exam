# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z ]{3,}$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$')

# Create your models here.
class UsersDBManager(models.Manager):
    def validate(self, data):
        errors = []
        unique = Users.objects.filter(username=data['username'])
        if len(data['name']) < 3:
            errors.append('Name must atleast 3 characters')
        if len(data['username']) < 3:
            errors.append('Username must atleast 3 characters')
        if not re.match(NAME_REGEX, data['name']):
            errors.append('Name fields can only contain letters')
        if not re.match(PASSWORD_REGEX, data['psw']) or len(data['psw']) < 8:
            errors.append('Password must be at least 8 characters and contain a lowercase, uppercase, number and symbol ')
        if data['psw'] != data['confpsw']:
            errors.append('Passwords do not match')
        if unique:
            errors.append('Invalid username address please select a different one')
        if errors:
            return [False, errors]
        else:
            psw = data['psw'].encode()
            hash_psw = bcrypt.hashpw(psw, bcrypt.gensalt())
            Users.objects.create(name=data['name'], username=data['username'], hash_psw=hash_psw)
            newUser = Users.objects.filter(username=data['username'])
            return [True, newUser[0]]

    def login(self, data):
        errors = []
        verify = Users.objects.filter(username=data['username'])
        psw = data['psw'].encode()
        hash_psw = bcrypt.hashpw(psw, bcrypt.gensalt())
        if not verify:
            errors.append('Invalid username or password')
        elif not bcrypt.checkpw(data['psw'].encode(), verify[0].hash_psw.encode()):
            errors.append('Invalid username or password')
        if errors:
            return [False, errors]
        else:
            return [True, verify[0]]

class Users(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    hash_psw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersDBManager()
