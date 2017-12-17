# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.shortcuts import render, get_object_or_404
from flightapp.models import *
import time
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import requests
import math
import datetime
# Create your views here.


def flights(request):
    if request.method == "POST":
#--AIRPORTS--
        with open('/home/liz/ListOfAirports.json') as data_file:
            data = json.load(data_file)
        for a in data['Airport']:
            if not (Airport.objects.filter(airport__startswith=a['code']).exists()):
                Airport.objects.create(airport=a['code'],
                                       airport_longitude=float(a['lon']),
                                       airport_latitude=float(a['lat']),
                                       airport_city=a['city'])
    air = Airport.objects.all()
    fly = Flight.objects.all()
    return render(request, 'flightapp/flights.html', {'air': air, 'fly': fly})


def selectview(request):
    air = Airport.objects.all()
    if request.method == 'POST':
        selected_air = get_object_or_404(Airport, pk=request.POST.get('airport_id'))
    return render('flightapp/flights.html', {'air': air}, {'selected_air':selected_air})


def koordinates():
    # pi - число pi, rad - радиус сферы (Земли)
    rad = 6372795
    # координаты двух точек
    llat1 = 77.1539
    llong1 = -120.398
    llat2 = 77.1804
    llong2 = 129.55
    # в радианах
    lat1 = llat1 * math.pi / 180.
    lat2 = llat2 * math.pi / 180.
    long1 = llong1 * math.pi / 180.
    long2 = llong2 * math.pi / 180.
    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)
    # вычисления длины большого круга
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    dist = ad * rad
    # вычисление начального азимута
    x = (cl1 * sl2) - (sl1 * cl2 * cdelta)
    y = sdelta * cl2
    z = math.degrees(math.atan(-y / x))
    print('z', z)
    if (x < 0):
        z = z + 180.
    z2 = (z + 180.) % 360. - 180.
    print('z2', z)
    z2 = - math.radians(z2)
    anglerad2 = z2 - ((2 * math.pi) * math.floor((z2 / (2 * math.pi))))
    #angledeg = (anglerad2 * 180.) / math.pi
    angledeg = math.atan(sdelta*cl2/(cl1*sl2-sl1*cl2*cdelta))
    c = math.pi / 180.
    dist = math.atan(
     (cl2*sdelta*math.sin(angledeg)+(cl1*sl2-sl1*cl2*cdelta)*math.cos(angledeg))/
     sl1*sl2+cl1*cl2*cdelta)
    print 'Distance >> %.0f' % dist, ' [meters]'
    print 'Initial bearing >> ', angledeg, '[degrees]'
    #new_lat = llat1 + dist * math.cos(angledeg * math.pi / 180) / (6371000 * math.pi / 180)
    #new_lon = llong1 + dist * math.sin(angledeg * math.pi / 180) / math.cos(lat1 * math.pi / 180) / (6371000 * math.pi / 180)
    cdist = math.cos(dist/rad*c)
    sdist = math.sin(dist/rad*c)
    new_lat = math.asin((sl1*cdist)+(cl1*sdist*math.cos(angledeg*c)))*(180/math.pi)
    y = sdist*math.sin(angledeg*c)
    x = cl1*cdist-sl1*sdist*math.cos(angledeg*c)
    new_lon = llong1 + math.atan2(y, x)
    print('  ', llat2, '(', lat2, ') lon', llong2, '(', long2, ')')
    nnew_lat = new_lat * math.pi / 180.
    nnew_lon = new_lon * math.pi / 180.
    print('new_lat', new_lat, ' ', nnew_lat)
    print('new_lon', new_lon, ' ', nnew_lon)


def validate_airport(request):
    selected_airport = request.GET.get('id')
    select_airport = Airport.objects.get(id=selected_airport)
#    koordinates()

    Flight.objects.filter(time_to__lte=time.time()).delete()

    if Flight.objects.filter(airport_from__startswith=select_airport.airport).count() < 7:
        print('i do request!!!!!!!!!!!!!')
        username = "ElizabethSkr"
        aiportcode = select_airport.airport
        apiKey = "815e7c0e54aa0c79d3ad1602597e5c05bd605869"
        fxmlUrl = "https://flightxml.flightaware.com/json/FlightXML3/"
        payload = {'airport_code': aiportcode, 'type': 'departures'}
        response = requests.get(fxmlUrl + "AirportBoards", params=payload, auth=(username, apiKey))
        if response.status_code == 200:
            decodedResponse = response.json()
            for flight in decodedResponse['AirportBoardsResult']['departures']['flights']:
                if Airport.objects.filter(airport__startswith=flight['destination']['alternate_ident']).exists() and \
                                flight['filed_arrival_time']['epoch'] > time.time() and \
                                flight['destination']['alternate_ident'] != '':
                    Flight.objects.create(airport_from=flight['origin']['alternate_ident'],
                                          city_from=flight['origin']['city'],
                                          time_from=flight['filed_departure_time']['epoch'],
                                          airport_to=flight['destination']['alternate_ident'],
                                          city_to=flight['destination']['city'],
                                          time_to=flight['filed_arrival_time']['epoch'],
                                          code_flight=flight['ident'],
                                          enrote=True)
               #   else:
               #       print ("There was an error retrieving the data from the server.")

    print('Flights:')
    flight = Flight.objects.filter(airport_from__startswith=select_airport.airport)
    line_flights = []
    for q in flight:
        myjson3 = {
            'airport_from': q.airport_from,
            'city_from': q.city_from,
            'airport_to': q.airport_to,
            'city_to': q.city_to,
            'lat_to': Airport.objects.get(airport=q.airport_to).airport_latitude,
            'lon_to': Airport.objects.get(airport=q.airport_to).airport_longitude,
            'code_flight': q.code_flight,
            'time_of_flight': abs(q.time_to-time.time()),
            'flight_from': abs(q.time_from),
            'flight_to': abs(q.time_to)
        }
        line_flights.append(myjson3)

    line_airports_to = []
    for q in flight:
        air = Airport.objects.get(airport=q.airport_to)
        myjson3 = {
            'airport': air.airport,
            'airport_city': air.airport_city,
            'airport_longitude': air.airport_longitude,
            'airport_latitude': air.airport_latitude,
        }
        line_airports_to.append(myjson3)

    data = {
        'is_taken_airport': select_airport.airport,
        'is_taken_city': select_airport.airport_city,
        'is_taken_lon': select_airport.airport_longitude,
        'is_taken_lat': select_airport.airport_latitude,
        'arr_flights': line_flights,
        'arr_airports_to': line_airports_to,
    }
    return JsonResponse(data)
