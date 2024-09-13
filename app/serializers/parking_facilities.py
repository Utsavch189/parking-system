from rest_framework import serializers
from app.models import FacilityChargesForArea
from .facilities import SlotFacilitySerializer

class FacilityChargesForAreaSerializer(serializers.ModelSerializer):
    
    facility=SlotFacilitySerializer(many=False)

    class Meta:
        model=FacilityChargesForArea
        fields=(
            'uid',
            'charges',
            'penalty_charge_per_hour',
            'facility',
            'last_updated_by',
            'updated_at',
            'created_at'
        )