from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry
import json
from django.db import connection
from datetime import date
# Create your views here.

from rest_framework import generics

from .models import MapCity
from .serializers import CitySerializer

#ListCreateAPIView
class CityList(generics.ListAPIView):
    queryset = MapCity.objects.all()
    serializer_class = CitySerializer
    connection.close()

#RetrieveUpdateDestroyAPIView
class CityDetail(generics.RetrieveAPIView):
    #ueryset = MapCity.objects.all()
    queryset = MapCity.objects.all()
    serializer_class = CitySerializer
    connection.close()


def create_city(request):
    with open('./seoul.geojson') as json_file:
        json_data = json.load(json_file)
        for data in json_data['features']:
            print(data)
            pnt = GEOSGeometry(str(data['geometry']))
            city = MapCity(sigungu_en= data['properties']['SIG_ENG_NM'], sigungu_kr=data['properties']['SIG_KOR_NM'], geometry=pnt)
            city.save()
    return render(request)


def city_info(request):
    cities = MapCity.objects.all()
    total_new = 0
    total_accumulation = 0
    for city in cities:
        total_new = total_new + city.new
        total_accumulation = total_accumulation + city.accumulation
    connection.close()
    today = date.today()
    return render(request, 'map.html', {'cities': cities, 'total_new': total_new, 'total_accumulation': total_accumulation, 'today': today.isoformat()})

def city_detail(request,id):
    cities = MapCity.objects.all()
    result = MapCity.objects.get(id=id)
    connection.close()
    return render(request, 'map_detail.html', {'city': result,'cities' : cities, 'id': id})