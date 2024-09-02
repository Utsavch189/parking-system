from rest_framework import serializers
from app.models import ParkingAreaOpenCloseTime

class ParkingTimingsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ParkingAreaOpenCloseTime
        fields=(
            'uid',
            'day',
            'open_time',
            'close_time'
        )