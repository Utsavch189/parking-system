from rest_framework import serializers
from app.models import ParkingSlotOpenCloseTime

class ParkingSlotTimingsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ParkingSlotOpenCloseTime
        fields=(
            'uid',
            'day',
            'open_time',
            'close_time'
        )