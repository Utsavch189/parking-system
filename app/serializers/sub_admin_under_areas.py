from rest_framework import serializers
from app.models import SubAdminUnderParkingArea
from .parking_areas import ParkingAreaSerializer

class SubAdminUnderParkingAreaSerializer(serializers.ModelSerializer):
    parking_area=ParkingAreaSerializer(many=False)
    class Meta:
        model=SubAdminUnderParkingArea
        fields=(
            'uid',
            'parking_area',
            'assigned_at',
            'is_verified',
            'is_suspended'
        )