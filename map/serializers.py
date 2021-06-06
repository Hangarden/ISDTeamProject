from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from . import models


class CitySerializer(GeoFeatureModelSerializer):

    class Meta:
        geo_field = "geometry"
        fields = ('id', 'sigungu_en', 'sigungu_kr','geometry', 'accumulation', 'new','CONTACT_HISTORY','related_gu')
        model = models.MapCity
