from django.shortcuts import render
from .api import check_air
# from .api import tags
import pandas
import numpy

def create(request):
    res = check_air()
    for gu in res.keys():
        city = MapCity.objects.get(sigunguKR=gu)
        city.related_gu = res[gu]
        city.save()
    return render(request, 'example.html', context)