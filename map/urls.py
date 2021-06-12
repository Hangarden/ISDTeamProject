from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create_city),
    path('', views.city_info, name = 'list_maps'),
    path('city/<int:id>', views.city_detail),
    path('api/', views.CityList.as_view()),
    path('api/detail/<int:pk>', views.CityDetail.as_view()),
]

