from django.urls import path

from . import views

app_name = 'keywords'

urlpatterns = [
    path('update/', views.update, name='index')
]