from django.shortcuts import render
from .api import check_air
# from .api import tags
import pandas
import numpy
from map.models import MapCity


def create(request):
    related = related_json()
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

    post = MapCity.objects.all()
    rank = ranked_json()
    context = {'post': post, 'rank': rank}
    return render(request, 'example.html', context)




