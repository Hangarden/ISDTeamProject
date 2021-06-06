from django.urls import path

from . import views

app_name = 'keywords'

urlpatterns = [
    path('create/', views.create, name='index')
]