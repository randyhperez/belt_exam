# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..logRegApp.models import Users

# Create your models here.
class TripManager(models.Manager):
    #Validates user input. If invalid entries returns with errors. If not returns True
    def create_trip(self, data, id):
        errors = []
        if len(data['destination']) < 1:
            errors.append('Please enter a destination')
        if len(data['description']) < 1:
            errors.append('please enter a description')
        if data['start'] > data['end']:
            errors.append('Start date must be before end date')
        if len(data['start']) < 1 or len(data['end']) < 1:
            errors.append('Please enter a start and end date')
        if errors:
            return [False, errors]
        else:
            Trip.objects.create(destination=data['destination'], description=data['description'], date_start=data['start'], date_end=data['end'], owner=Users.objects.get(id=id))
            return [True]

    # returns users created // joined trips for dashboard page
    def get_trips(self, id):
        trips = Trip.objects.filter(owner_id=id)| Trip.objects.filter(joined_by__id=id)
        return trips.order_by('date_start')

    def get_other_trips(self, id):
        return Trip.objects.all().exclude(joined_by=Users.objects.get(id=id))

    def trip_join(self, trip_id, user_id):
        unique = Trip.objects.filter(id=trip_id, joined_by__id=user_id)
        if unique:
            return [False, 'You have already Joined this trip']
        else:
            this_trip = Trip.objects.get(id=trip_id)
            this_trip.joined_by.add(Users.objects.get(id=user_id))
            return [True]

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    owner = models.ForeignKey(Users, related_name='trip_owner', on_delete=models.CASCADE)
    joined_by = models.ManyToManyField(Users, related_name='joined_trip')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
