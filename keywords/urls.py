from django.urls import path

from . import views

app_name = 'keywords'

urlpatterns = [
    path('', views.index, name='index')
]