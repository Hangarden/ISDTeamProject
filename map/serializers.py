from rest_framework import serializers
from . import models


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'sigungu_en', 'sigungu_kr','geometry', 'accumulation', 'new','CONTACT_HISTORY','related_gu')
        model = models.MapCity
