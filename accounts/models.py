from django.db import models
from django.contrib.auth.models import  User
from map.models import MapCity

class Residence(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(MapCity, on_delete=models.CASCADE)
