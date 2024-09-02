from rest_framework import serializers
from app.models import ParkingArea
from .parking_facilities import FacilityChargesForAreaSerializer
from .parking_timings import ParkingTimingsSerializer

class ParkingAreaSerializer(serializers.ModelSerializer):
    facilities=FacilityChargesForAreaSerializer(many=True,source='facilities_for_areas')
    timings=ParkingTimingsSerializer(many=True,source='parking_area_timings')
    
    class Meta:
        model=ParkingArea
        fields=(
            'uid',
            'area_name',
            'parking_owner_register_qr',
            'searchingslots_qr',
            'facilities',
            'timings',
            'created_at',
            'is_suspended'
        )