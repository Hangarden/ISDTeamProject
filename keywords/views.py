from django.http import JsonResponse
from django.shortcuts import render, redirect
from .api import x_json, related_json, confirmed_json, all_json, ranked_json
from map.models import MapCity
from django.db import connection

# 해당 구의 금일 총 확진자수와 증가된 확진자수, 관련 구 확진자수를 Mapcity에 입력.
# column을 추가해야해서 migrate 필요할 수도..?


def update(request):
    x = x_json()
    related = related_json(x)
    for gu in related.keys():
        city = MapCity.objects.get(sigungu_kr=gu)
        city.related_gu = related[gu]
        city.save()

    confirmed = confirmed_json()
    for gu in confirmed.keys():
        city = MapCity.objects.get(sigungu_kr=gu)
        city.accumulation = int(confirmed[gu][1])
        city.new = int(confirmed[gu][2])
        city.save()

    all = all_json()
    rank = ranked_json(all)
    for gu in rank.keys():
        city = MapCity.objects.get(sigungu_kr=gu)
        city.CONTACT_HISTORY = rank[gu]
        city.save()

    connection.close()
    return JsonResponse({
        'status': 201,
        'message': 'update contact complete',
    }, json_dumps_params = {'ensure_ascii': True})

