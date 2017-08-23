"""
The login app has 4 functions to assist the user, including
registering, and login. Registration validations are in the
model.py for the login app.
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(request):
    """This is the main index page"""
    if request.session.get('id'):
        return redirect('quotes:index')
    return render(request, 'login/index.html')

def register(request):
    """When a user registers, send to model"""
    results = User.objects.registervalidate(request.POST)
    if not results['status']:
        for error in results['errors']:
            messages.error(request, error)
            return redirect('auth:index')
    request.session['id'] = results['user'].id
    return redirect('quotes:index')

def login(request):
    """When user logs in, send to model for validations"""
    results = User.objects.loginvalidate(request.POST)
    if results['status'] is False:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('auth:index')
    else:
        user = User.objects.get(id=results['user'])
        request.session['id'] = user.id
    return redirect('quotes:index')

def logout(request):
    """Logout will flush session data!!!"""
    request.session.flush()
    messages.success(request, 'Logged Out')
    return redirect('auth:index')

