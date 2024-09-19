from rest_framework import serializers
from app.models import ParkingSlotWithFacilities
from .facilities import SlotFacilitySerializer

class SlotFacilitiesSerializer(serializers.ModelSerializer):

    facility=SlotFacilitySerializer(many=False)
    
    class Meta:
        model=ParkingSlotWithFacilities
        fields=(
            'uid',
            'parking_slot',
            'facility',
            'assigned_at'
        )