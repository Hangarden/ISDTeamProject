from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry
from rest_framework_gis.pagination import GeoJsonPagination
from map.models import MapCity
import json
from django.http import HttpResponse

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


