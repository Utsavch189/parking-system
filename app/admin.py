from django.contrib import admin
from .models import (
    Role, SuperAdmin, Admin, SubAdmin, ParkingOwner, ParkingArea,
    SubAdminUnderParkingArea, SlotFacility,FacilityChargesForArea, ParkingSlot,
    ParkingSlotOpenCloseTime,ParkingAreaOpenCloseTime, ParkingSlotWithFacilities,
    SlotUnderParkingArea, Car, ArrivalDepart, AdminChangingHistoryParkingAreas,
    OTP,TwoFactorVerification,CountryCode,EmailVerifyLinkSession,CdnFileManager,ErrorLog,AccessLog
)

class RoleView(admin.ModelAdmin):
    list_display=('uid','role_name','ui_name','level','is_active')
    def get_queryset(self, request):
        return Role.admin_objects.all()

class SuperAdminView(admin.ModelAdmin):
    list_display=('uid','name','email','is_active')
    def get_queryset(self, request):
        return SuperAdmin.admin_objects.all()

class AdminView(admin.ModelAdmin):
    list_display=('uid','name','email','pincode','country_code','is_active','is_suspended','created_at')
    def get_queryset(self, request):
        return Admin.admin_objects.all()

class SubAdminView(admin.ModelAdmin):
    list_display=('uid','name','email','pincode','country_code','is_active','is_suspended','created_at')
    def get_queryset(self, request):
        return SubAdmin.admin_objects.all()

class ParkingOwnerView(admin.ModelAdmin):
    list_display=('uid','name','email','pincode','country_code','is_active','is_suspended','created_at')
    def get_queryset(self, request):
        return ParkingOwner.admin_objects.all()

class ParkingAreaView(admin.ModelAdmin):
    list_display=('uid','area_name','admin_name','is_active','is_suspended','created_at')
    
    def get_queryset(self, request):
        return ParkingArea.admin_objects.all()
    
    def admin_name(self, obj):
        return obj.admin.name if obj.admin else 'N/A'
    admin_name.short_description = 'Admin'

class SubAdminUnderParkingAreaView(admin.ModelAdmin):
    list_display=('uid','sub_admin_name','admin_name','parking_area_name','assigned_at','is_active','is_suspended')
    
    def get_queryset(self, request):
        return SubAdminUnderParkingArea.admin_objects.all()
    
    def sub_admin_name(self, obj):
        return obj.sub_admin.name if obj.sub_admin else 'N/A'
    sub_admin_name.short_description = 'Sub Admin'

    def admin_name(self, obj):
        return obj.admin.name if obj.admin else 'N/A'
    admin_name.short_description = 'Admin'

    def parking_area_name(self, obj):
        return obj.parking_area.area_name if obj.parking_area else 'N/A'
    parking_area_name.short_description = 'Parking Area'

class SlotFacilityView(admin.ModelAdmin):
    list_display=('uid','facility_name','facility_value','created_by','is_active','created_at')
    
    def get_queryset(self, request):
        return SlotFacility.admin_objects.all()
    
    def created_by(self, obj):
        return obj.created_by.name if obj.created_by else 'N/A'
    created_by.short_description = 'created_by'

class FacilityChargesForAreaView(admin.ModelAdmin):
    list_display=('uid','charges','penalty_charge_per_hour','facility','area','is_active','created_at','updated_at','last_updated_by')

    def get_queryset(self, request):
        return FacilityChargesForArea.admin_objects.all()
    
    def get_facility(self,obj):
        return obj.facility.facility_name if obj.facility else 'N/A'
    get_facility.short_description = 'facility'

    def get_area(self,obj):
        return obj.area.area_name if obj.area else 'N/A'
    get_area.short_description = 'area'

    def get_last_updated_by(self,obj):
        return obj.last_updated_by.name if obj.last_updated_by else 'N/A'
    get_last_updated_by.short_description = 'last_updated_by'

class ParkingSlotView(admin.ModelAdmin):
    list_display=('uid','slot_no','address','slot_creator','is_active','created_at','is_suspended')

    def get_queryset(self, request):
        return ParkingSlot.admin_objects.all()

    def get_slot_creator(self,obj):
        return obj.slot_creator.name if obj.slot_creator else 'N/A'
    get_slot_creator.short_description='slot_creator'

class ParkingSlotOpenCloseTimeView(admin.ModelAdmin):
    list_display=('uid','slot','day','open_time','close_time','is_active')

    def get_queryset(self, request):
        return ParkingSlotOpenCloseTime.admin_objects.all()
    
    def get_slot(self,obj):
        return f"{obj.slot.slot_no} {obj.slot.address}" if obj.slot else 'N/A'
    get_slot.short_description='slot'

class ParkingAreaOpenCloseTimeView(admin.ModelAdmin):
    list_display=('uid','area','open_time','close_time','is_active')

    def get_queryset(self, request):
        return ParkingAreaOpenCloseTime.admin_objects.all()
    
    def get_area(self,obj):
        return obj.area.area_name if obj.area else 'N/A'
    get_area.short_description = 'area'

class ParkingSlotWithFacilitiesView(admin.ModelAdmin):
    list_display=('uid','parking_slot','facility','assigned_at','is_active')

    def get_queryset(self, request):
        return ParkingSlotWithFacilities.admin_objects.all()
    
    def get_parking_slot(self,obj):
        return f"{obj.parking_slot.slot_no} {obj.parking_slot.address}" if obj.parking_slot else 'N/A'
    get_parking_slot.short_description='parking_slot'

    def get_facility(self,obj):
        return obj.facility.facility_name if obj.facility else 'N/A'
    get_facility.short_description='facility'

class SlotUnderParkingAreaView(admin.ModelAdmin):
    list_display=('uid','area','slot','assigned_at','is_verified','approved_by','is_active')

    def get_queryset(self, request):
        return SlotUnderParkingArea.admin_objects.all()
    
    def get_area(self,obj):
        return obj.area.area_name if obj.area else 'N/A'
    get_area.short_description = 'area'

    def get_slot(self,obj):
        return f"{obj.slot.slot_no} {obj.slot.address}" if obj.slot else 'N/A'
    get_slot.short_description='slot'

    def get_approved_by(self,obj):
        return obj.approved_by.name if obj.approved_by else 'N/A'
    get_approved_by.short_description='approved_by'

class CarView(admin.ModelAdmin):
    list_display=('uid','owner_name','owner_email','owner_phone','car_no','car_pic','owner_pic','is_active')

    def get_queryset(self, request):
        return Car.admin_objects.all()
    

class ArrivalDepartView(admin.ModelAdmin):
    list_display=('uid','car','parking_slot','area','arrival_time','release_code','expected_depart_time','actual_depart_time','is_active')

    def get_queryset(self, request):
        return ArrivalDepart.admin_objects.all()
    
    def get_car(self,obj):
        return obj.car.car_no if obj.car else 'N/A'
    get_car.short_description='car'

    def get_parking_slot(self,obj):
        return f"{obj.parking_slot.slot_no} {obj.parking_slot.address}" if obj.parking_slot else 'N/A'
    get_parking_slot.short_description='parking_slot'

    def get_area(self,obj):
        return obj.area.area_name if obj.area else 'N/A'
    get_area.short_description = 'area'

class AdminChangingHistoryParkingAreasView(admin.ModelAdmin):
    list_display=('uid','prev_admin','current_admin','parking_area','changed_by','assigned_at','is_active')

    def get_queryset(self, request):
        return AdminChangingHistoryParkingAreas.admin_objects.all()

    def get_prev_admin(self,obj):
        return obj.prev_admin.name if obj.prev_admin else 'N/A'
    get_prev_admin.short_description='prev_admin'

    def get_current_admin(self,obj):
        return obj.current_admin.name if obj.current_admin else 'N/A'
    get_current_admin.short_description='current_admin'

    def get_parking_area(self,obj):
        return obj.parking_area.area_name if obj.parking_area else 'N/A'
    get_parking_area.short_description = 'parking_area'

    def get_changed_by(self,obj):
        return obj.changed_by.name if obj.changed_by else 'N/A'
    get_changed_by.short_description='changed_by'


class OTPView(admin.ModelAdmin):
    list_display=('user_id','otp','created_at','will_expire_at','is_active')

    def get_queryset(self, request):
        return OTP.admin_objects.all()

class TwoFactorVerificationView(admin.ModelAdmin):
    list_display=('user_id','qr_path','created_at','is_active')

    def get_queryset(self, request):
        return TwoFactorVerification.admin_objects.all()

class CountryCodeView(admin.ModelAdmin):
    list_display=('country','country_code','iso_code','is_active')

    def get_queryset(self, request):
        return CountryCode.admin_objects.all()

admin.site.register(Role,RoleView)
admin.site.register(SuperAdmin,SuperAdminView)
admin.site.register(Admin,AdminView)
admin.site.register(SubAdmin,SubAdminView)
admin.site.register(ParkingOwner,ParkingOwnerView)
admin.site.register(ParkingArea,ParkingAreaView)
admin.site.register(SubAdminUnderParkingArea,SubAdminUnderParkingAreaView)
admin.site.register(SlotFacility,SlotFacilityView)
admin.site.register(FacilityChargesForArea,FacilityChargesForAreaView)
admin.site.register(ParkingSlot,ParkingSlotView)
admin.site.register(ParkingSlotOpenCloseTime,ParkingSlotOpenCloseTimeView)
admin.site.register(ParkingAreaOpenCloseTime,ParkingAreaOpenCloseTimeView)
admin.site.register(ParkingSlotWithFacilities,ParkingSlotWithFacilitiesView)
admin.site.register(SlotUnderParkingArea,SlotUnderParkingAreaView)
admin.site.register(Car,CarView)
admin.site.register(ArrivalDepart,ArrivalDepartView)
admin.site.register(AdminChangingHistoryParkingAreas,AdminChangingHistoryParkingAreasView)
admin.site.register(OTP,OTPView)
admin.site.register(TwoFactorVerification,TwoFactorVerificationView)
admin.site.register(CountryCode,CountryCodeView)
admin.site.register(EmailVerifyLinkSession)
admin.site.register(CdnFileManager)
admin.site.register(AccessLog)
admin.site.register(ErrorLog)