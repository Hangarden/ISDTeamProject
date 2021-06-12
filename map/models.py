from django.contrib.gis.db import models

# Create your models here.


class MapCity(models.Model):
    id = models.BigAutoField(primary_key=True)
    sigungu_en = models.CharField(db_column='sigungu_EN', max_length=200)  # Field name made lowercase.
    sigungu_kr = models.CharField(db_column='sigungu_KR', max_length=200)  # Field name made lowercase.
    geometry = models.GeometryField()
    accumulation = models.IntegerField(default=0)
    new = models.IntegerField(default=0)
    CONTACT_HISTORY = models.JSONField(null=True, blank=True)
    related_gu = models.JSONField(null=True, blank=True)


class CountStatus(models.Model):
    city = models.ForeignKey(MapCity, on_delete=models.CASCADE)
    add = models.IntegerField(default=0)
    accumulation = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
