from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry
from map.models import MapCity
import json
# Create your views here.


def create_city(request):
    with open('./seoul.geojson') as json_file:
        json_data = json.load(json_file)
        for data in json_data['features']:
            print(data)
            pnt = GEOSGeometry(str(data['geometry']))
            city = MapCity(sigungu_en= data['properties']['SIG_ENG_NM'], sigungu_kr=data['properties']['SIG_KOR_NM'], geometry=pnt)
            city.save()
    return render(request)
