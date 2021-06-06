from django.urls import path

from map import views

urlpatterns = [
    path('', views.create_city, name = 'create_city'),
]
