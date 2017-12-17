# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Airport(models.Model):
    airport = models.CharField(max_length=3)
    airport_longitude = models.FloatField()
    airport_latitude = models.FloatField()
    airport_city = models.CharField(max_length=50)


class Flight(models.Model):
    airport_from = models.CharField(max_length=3)
    city_from = models.CharField(max_length=50)
    time_from = models.IntegerField()
    airport_to = models.CharField(max_length=3)
    city_to = models.CharField(max_length=50)
    time_to = models.IntegerField()
    code_flight = models.CharField(max_length=10)
    enrote = models.BooleanField()

