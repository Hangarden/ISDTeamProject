from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create_city),
    path('', views.CityList.as_view()),
    path('detail/<int:pk>', views.CityDetail.as_view()),
]

