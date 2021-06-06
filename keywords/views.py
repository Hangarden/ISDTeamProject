from django.shortcuts import render
from .api import check_air
# from .api import tags
import pandas
import numpy

def index(request):
    res = check_air()
    d = keyword(res)

    context = {'pm10': 'pm10'}
    return render(request, 'example.html', context)
