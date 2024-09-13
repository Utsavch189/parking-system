from rest_framework import serializers
from app.models import SubAdmin
from .sub_admin_under_areas import SubAdminUnderParkingAreaSerializer

class SubAdminSerializer(serializers.ModelSerializer):
    associate_areas=SubAdminUnderParkingAreaSerializer(many=True,source='subadmin')
    class Meta:
        model=SubAdmin
        fields=(
            'uid',
            'name',
            'email',
            'phone',
            'pincode',
            'country_code',
            'role',
            'associate_areas',
            'is_verified',
            'is_suspended',
            'created_at'
        )