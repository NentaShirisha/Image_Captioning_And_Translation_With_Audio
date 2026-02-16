from rest_framework import serializers
from .models import CaptionHistory

class CaptionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaptionHistory
        fields = '__all__'