from rest_framework import serializers
from app.models import SlotFacility

class SlotFacilitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model=SlotFacility
        fields=(
            'uid',
            'facility_name',
            'facility_value',
            'created_by',
            'created_at'
        )