# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import User
from models import Quote

def index(request):
    try:
        request.session['id']
    except KeyError:
        request.session.flush()
        messages.error(request, 'There is user session detected, please login.')
        return redirect('auth:index')
    loggedinuser = User.objects.get(id=request.session['id'])
    favoritequote = Quote.objects.filter(favorite = request.session['id'])
    quotablequotes = Quote.objects.all().exclude(favorite = request.session['id'])
    context = {
        'loggedinuser': loggedinuser,
        'quotablequotes': quotablequotes,
        'favoritequotes': favoritequote
    }
    return render(request, 'quotes/index.html', context)

def newQuote(request):
    insertnewquote = Quote.objects.insertnewquote(request.POST)
    if len(insertnewquote) > 0:
        for error in insertnewquote:
            messages.error(request, error)
            print error
    return redirect('/quotes')
        

    # return redirect('quotes:index')

def addFavorite(request):
    insertfavorite = Quote.objects.insertfavorite(request.POST)
    if not insertfavorite['status']:
        for error in insertfavorite['errors']:
            messages.error(request, error)
    return redirect('quotes:index')

def removeFavorite(request):
    removefavorite = Quote.objects.removefavorite(request.POST)
    if not removefavorite['status']:
        for error in removefavorite['errors']:
            messages.error(request, error)
    return redirect('quotes:index')

def showUser(request, userid):
    try:
        request.session['id']
    except KeyError:
        request.session.flush()
        messages.error(request, 'There is user session detected, please login.')
        return redirect('auth:index')
    user = User.objects.get(id=userid)
    quotes = Quote.objects.filter(created_by=userid)
    context = {
        'user': user,
        'quotes': quotes
    }
    return render(request, 'quotes/showUser.html', context)
