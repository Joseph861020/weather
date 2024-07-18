from rest_framework import serializers

from .models import CitySearchHistory


class CitySearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CitySearchHistory
        fields = '__all__'
