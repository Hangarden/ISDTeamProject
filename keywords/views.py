from django.shortcuts import render
from .api import check_air
# from .api import tags
import pandas
import numpy

def create(request):
    res = check_air()
    return render(request, 'example.html')
