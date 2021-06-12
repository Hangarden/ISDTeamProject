from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry
from django.http import HttpResponse, JsonResponse
from django.contrib.gis.db.models.functions import Centroid
import json
import requests
from django.db import connection
from datetime import date
import pandas as pd
# Create your views here.

from rest_framework import generics

from .models import MapCity, CountStatus
from .serializers import CitySerializer
from datetime import datetime


# ListCreateAPIView
class CityList(generics.ListAPIView):
    queryset = MapCity.objects.all()
    serializer_class = CitySerializer
    connection.close()


# RetrieveUpdateDestroyAPIView
class CityDetail(generics.RetrieveAPIView):
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


def update_count_status(request):
    last_day = CountStatus.objects.order_by('-date').first()
    time_diff = (date.today() - last_day.date.date()).days
    len_today_update = len(CountStatus.objects.filter(date=date.today()))
    if len_today_update > 0 and time_diff == 0:
        return JsonResponse({
            'status': 200,
            'message': 'already update',
            }, json_dumps_params = {'ensure_ascii': True})
    if len_today_update == 0 and time_diff == 0:
        time_diff = 1
    else:
        print('time_diff: ', time_diff)
        url = f"http://openapi.seoul.go.kr:8088/587671694b6169723631477470454d/json/TbCorona19CountStatusJCG/1/{time_diff}"
        print(url)
        res = requests.get(url)
        data = res.text
        rows = json.loads(data)['TbCorona19CountStatusJCG']['row']
        cities = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구', '양천구',
              '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', '서초구', '강남구', '송파구', '강동구']
        for rowLen in range(0, len(rows)):
            dicts = dict()
            for i in range(0, len(cities)):
                dicts[cities[i]] = [list(rows[rowLen].values())[0], list(rows[rowLen].values())[2*i+1], list(rows[rowLen].values())[2*i+2]]
            print(dicts)
            for gu in dicts.keys():
                replaceDate = ".".join(dicts[gu][0].split('.')[0:-1])
                print(replaceDate)
                city = MapCity.objects.get(sigungu_kr=gu)
                city_count_status = CountStatus(
                city=city,
                add=dicts[gu][2],
                accumulation=dicts[gu][1],
                date=datetime.strptime(replaceDate, "%Y.%m.%d")
                )
                city_count_status.save()
    return JsonResponse({
        'status': 201,
        'message': 'update CountStatus complete',
    }, json_dumps_params = {'ensure_ascii': True})


def city_info(request):
    cities = MapCity.objects.all()
    total_new = 0
    total_accumulation = 0
    print(len(cities))
    for city in cities:
        total_new = total_new + city.new
        total_accumulation = total_accumulation + city.accumulation
    connection.close()
    today = date.today()
    return render(request, 'map.html', {'cities': cities, 'total_new': total_new, 'total_accumulation': total_accumulation, 'today': today.isoformat()})


def city_detail(request,id):
    cities = MapCity.objects.all()
    result = MapCity.objects.get(id=id)
    today = date.today()
    connection.close()
    center = result.geometry.centroid
    centerPnt = [float(center.ewkt.split(' ')[1].replace('(','')), float(center.ewkt.split(' ')[2].replace(')',''))]
    return render(request, 'map_detail.html', {'city': result,'cities' : cities, 'id': id, 'today': today, 'centerPnt': centerPnt})
