"""
This is the main processing model for the login/registration app. 
All user login and registration validations are done here. 
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import re
from django.db import models
import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def registervalidate(self, postData):
        """Main registration validations"""
        results = {'status': True, 'errors': [], 'user': None}
        if not postData['fname'] or len(postData['fname']) < 3:
            results['errors'].append("First Name must be at least 3 characters")
            results['status'] = False
        if not postData['lname'] or len(postData['lname']) < 3:
            results['errors'].append("Last Name must be at least 3 characters")
            results['status'] = False
        if not postData['alias'] or len(postData['alias']) < 3:
            results['errors'].append("Alias must be at least 3 characters")
            results['status'] = False
        if not postData['email'] or \
            not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", postData['email']):
            results['errors'].append("Email Address is not valid")
            results['status'] = False
        if not postData['dob']:
            results['errors'].append("Birthday is required")
            results['status'] = False
        if not postData['userpassword'] or len(postData['userpassword']) < 8:
            results['errors'].append("Password must be at least 8 characters")
            results['status'] = False
        if postData['cpassword'] != postData['userpassword']:
            results['errors'].append("Passwords do not match")
            results['status'] = False
        user = User.objects.filter(email=postData['email'])
        if user:
            results['status'] = False
            results['errors'].append("Registration Failure, have you tried to login?")
        if results['status'] is False:
            return results
        if results['status']:
            userpassword = bcrypt.hashpw(postData['userpassword'].encode(), bcrypt.gensalt())
            user = User.objects.create(
                fname=postData['fname'],
                lname=postData['lname'],
                email=postData['email'],
                dob=postData['dob'],
                alias=postData['alias'],
                userpassword=userpassword)
            results['user'] = user
        return results

    def loginvalidate(self, postData):
        """login only validations"""
        results = {'status': True, 'errors': [], 'user': None}
        try:                # need this try loop if the db is empty.
            user = User.objects.filter(email=postData['email'])
            user[0] #This is an extra test to make sure the data is present
        except:
            results['status'] = False
            results['errors'].append("Account or password failure.")
            return results
        if user[0]:
            if user[0].userpassword != bcrypt.hashpw(postData['userpassword'].encode(),
                                                     user[0].userpassword.encode()):
                results['status'] = False
                results['errors'].append("Account or password failure.")
            else:
                results['user'] = user[0].id
        else:
            results['status'] = False
        return results


class User(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    alias = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=100, unique=True)
    userpassword = models.CharField(max_length=100)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    objects = UserManager()
