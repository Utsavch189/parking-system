from rest_framework import serializers
from app.models import ParkingSlot
from .slot_facilities import SlotFacilitiesSerializer
from .slot_timings import ParkingSlotTimingsSerializer

class ParkingSlotSerializer(serializers.ModelSerializer):

    facilities=SlotFacilitiesSerializer(many=True,source='parking_slots')
    timings=ParkingSlotTimingsSerializer(many=True,source='parking_slots_timings')

    class Meta:
        model=ParkingSlot
        fields=(
            'uid',
            'name',
            'slot_no',
            'address',
            'direction_guidance',
            'facilities',
            'timings',
            'slot_creator',
            'slot_booking_qr',
            'is_suspended',
            'created_at'
        )