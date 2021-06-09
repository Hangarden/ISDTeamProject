from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry
import json
from django.db import connection

# Create your views here.

from rest_framework import generics

from .models import MapCity
from .serializers import CitySerializer

#ListCreateAPIView
class CityList(generics.ListAPIView):
    queryset = MapCity.objects.all()
    serializer_class = CitySerializer

#RetrieveUpdateDestroyAPIView
class CityDetail(generics.RetrieveAPIView):
    #ueryset = MapCity.objects.all()
    queryset = MapCity.objects.all()
    serializer_class = CitySerializer


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
    connection.close()
    return render(request, 'map.html', {'cities': cities})

def city_detail(request,id):
    result = MapCity.objects.get(id=id)
    connection.close()
    return render(request, 'map_detail.html', {'city': result})