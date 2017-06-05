# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render, redirect
from ..logRegApp.models import Users
from .models import Trip

# Create your views here.
def index(request):
    #check if user logged in
    if 'id' in request.session:
        return redirect('beltApp:dashboard')
    return render(request, 'beltApp/index.html')

#renders dashboard page
def dashboard(request):
    #check if user logged in
    if 'id' not in request.session:
        return redirect('beltApp:index')
    context = {
        'users_trips': Trip.objects.get_trips(request.session['id']),
        'others_trips': Trip.objects.get_other_trips(request.session['id']),
    }
    return render(request, 'beltApp/dashboard.html', context)

#Renders page w/ form to add new trip
def tripform(request):
    #check if user logged in
    if 'id' not in request.session:
        return redirect('beltApp:index')
    return render(request, 'beltApp/newtrip.html')

#Runs logic to validate // create new trip
def addTrip(request):
    if request.method == 'POST':
        response = Trip.objects.create_trip(request.POST, request.session['id'])
        #if user entry contained errors returns error messages
        if not response[0]:
            for error in response[1]:
                messages.error(request, error)
        #if user entry was accepted
        else:
            return redirect('beltApp:dashboard')
    return redirect('beltApp:tripform')

#Renders page with trip info and others who joined trip
def destination(request, id):
    #check if user logged in
    if 'id' not in request.session:
        return redirect('beltApp:index')
    context = {
        'trip': Trip.objects.get(id=id),
        'others': Users.objects.filter(joined_trip__id=id)
    }
    return render(request, 'beltApp/destination.html', context)

#User verifies they want to join trip
def verifyJoin(request, id):
    #check if user logged in
    if 'id' not in request.session:
        return redirect('beltApp:index')
    context = {
        'trip': Trip.objects.get(id=id)
    }
    return render(request, 'beltApp/verifyjoin.html', context)

#Runs logic to validate // join trip
def joinTrip(request, id):
    if request.method == 'POST':
        if request.POST['verify'] == 'yes':
            response = Trip.objects.trip_join(id, request.session['id'])
            #If user already has joined this speicific trip
            if not response[0]:
                messages.error(request, response[1])
    return redirect('beltApp:dashboard')

#User verifies if they want to delete a trip they created
def verifyDelete(request, id):
    #check if user logged in
    if 'id' not in request.session:
        return redirect('beltApp:index')
    context = {
        'trip': Trip.objects.get(id=id)
    }
    return render(request, 'beltApp/verifydelete.html', context)

#Deletes Trip
def deleteTrip(request, id):
    if request.method == 'POST':
        if request.POST['verify'] == 'yes':
            Trip.objects.get(id=id).delete()
    return redirect('beltApp:dashboard')
