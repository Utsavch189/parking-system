from django.db import models
from datetime import datetime
from .model_manager import ActiveManager,AdminManager
from django.contrib.auth.hashers import make_password,check_password

class Role(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    role_name=models.CharField(max_length=30,unique=True)
    level=models.IntegerField()
    ui_name=models.CharField(max_length=30,unique=True,default="",null=True,blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(default=datetime.now())

    objects = ActiveManager()
    admin_objects = AdminManager() 

    def save(self, *args, **kwargs):
        self.role_name=self.role_name.upper()
        if self.ui_name:
            self.ui_name=self.ui_name.upper()
        super(Role, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.role_name

class SuperAdmin(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)
    phone=models.CharField(max_length=10,unique=True)
    password=models.TextField()
    role=models.ForeignKey(Role,on_delete=models.SET_NULL,related_name='superadmin_role',null=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(default=datetime.now())

    objects = ActiveManager()
    admin_objects = AdminManager() 

    def save(self, *args, **kwargs):
        self.name=self.name.upper()
        self.email=self.email.lower()
        if not self.id:
            self.password=make_password(self.password)
        super(SuperAdmin, self).save(*args, **kwargs)
    
    def is_correct_password(self,password:str):
        return check_password(password,self.password)
    
    def __str__(self) -> str:
        return self.name

class Admin(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)
    phone=models.CharField(max_length=10,unique=True)
    password=models.TextField()
    pincode=models.IntegerField()
    country_code=models.CharField(max_length=30)
    role=models.ForeignKey(Role,on_delete=models.SET_NULL,related_name='admin_role',null=True)
    subadmin_register_qr=models.TextField(null=True,blank=True)
    is_active=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    is_suspended=models.BooleanField(default=False)
    created_at=models.DateTimeField(default=datetime.now())

    objects = ActiveManager()
    admin_objects = AdminManager() 

    def save(self, *args, **kwargs):
        self.name=self.name.upper()
        self.email=self.email.lower()
        if not self.id:
            self.password=make_password(self.password)
        super(Admin, self).save(*args, **kwargs)
    
    def is_correct_password(self,password:str):
        return check_password(password,self.password)
    
    def __str__(self) -> str:
        return self.name

class SubAdmin(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)
    phone=models.CharField(max_length=10,unique=True)
    password=models.TextField()
    pincode=models.IntegerField(default=0)
    country_code=models.CharField(max_length=30,default="")
    associate_admin=models.ForeignKey(Admin,on_delete=models.SET_NULL,related_name='sub_admin_associate_admin',null=True)
    role=models.ForeignKey(Role,on_delete=models.SET_NULL,related_name='subadmin_role',null=True)
    is_active=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    is_suspended=models.BooleanField(default=False)
    created_at=models.DateTimeField(default=datetime.now())

    objects = ActiveManager()
    admin_objects = AdminManager() 

    def save(self, *args, **kwargs):
        self.name=self.name.upper()
        self.email=self.email.lower()
        if not self.id:
            self.password=make_password(self.password)
        super(SubAdmin, self).save(*args, **kwargs)
    
    def is_correct_password(self,password:str):
        return check_password(password,self.password)
    
    def __str__(self) -> str:
        return self.name

class ParkingOwner(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)
    phone=models.CharField(max_length=10,unique=True)
    password=models.TextField()
    pincode=models.IntegerField(default=0)
    country_code=models.CharField(max_length=30,default="")
    role=models.ForeignKey(Role,on_delete=models.SET_NULL,related_name='powner_role',null=True)
    is_active=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    is_suspended=models.BooleanField(default=False)
    created_at=models.DateTimeField(default=datetime.now())

    objects = ActiveManager()
    admin_objects = AdminManager() 

    def save(self, *args, **kwargs):
        self.name=self.name.upper()
        self.email=self.email.lower()
        if not self.id:
            self.password=make_password(self.password)
        super(ParkingOwner, self).save(*args, **kwargs)
    
    def is_correct_password(self,password:str):
        return check_password(password,self.password)
    
    def __str__(self) -> str:
        return self.name

class ParkingArea(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    area_name=models.CharField(max_length=100)
    parking_owner_register_qr=models.TextField(null=True,blank=True)
    searchingslots_qr=models.TextField(null=True,blank=True)
    admin=models.ForeignKey(Admin,on_delete=models.CASCADE,related_name='area_under_admin')
    is_active=models.BooleanField(default=True)
    is_suspended=models.BooleanField(default=False)
    created_at=models.DateTimeField(default=datetime.now())

    objects = ActiveManager()
    admin_objects = AdminManager() 
    
    def __str__(self) -> str:
        return self.area_name

class SubAdminUnderParkingArea(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    sub_admin=models.ForeignKey(SubAdmin,on_delete=models.CASCADE,related_name='subadmin')
    admin=models.ForeignKey(Admin,on_delete=models.SET_NULL,related_name='subadmin_under_admin',null=True)
    parking_area=models.ForeignKey(ParkingArea,on_delete=models.SET_NULL,related_name='subadmin_under_parking_area',null=True)
    assigned_at=models.DateTimeField(default=datetime.now())
    is_active=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    is_suspended=models.BooleanField(default=False)

    objects = ActiveManager()
    admin_objects = AdminManager() 

class SlotFacility(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    facility_name=models.CharField(max_length=100)
    facility_value=models.CharField(max_length=100)
    created_by=models.ForeignKey(SuperAdmin,on_delete=models.CASCADE,related_name='slot_facility_created_by')
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(default=datetime.now())

    objects = ActiveManager()
    admin_objects = AdminManager() 

    def save(self, *args, **kwargs):
        self.facility_name=self.facility_name.upper()
        super(SlotFacility, self).save(*args, **kwargs)

class FacilityChargesForArea(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    charges=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    penalty_charge_per_hour=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    facility=models.ForeignKey(SlotFacility,on_delete=models.CASCADE,related_name='facility_under_area')
    area=models.ForeignKey(ParkingArea,on_delete=models.CASCADE,related_name='facilities_for_areas')
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(default=datetime.now())
    updated_at=models.DateTimeField(default=None,null=True,blank=True)
    last_updated_by=models.ForeignKey(Admin,on_delete=models.CASCADE,related_name='updated_facility_for_area_by',null=True,blank=True)

    objects = ActiveManager()
    admin_objects = AdminManager() 

class ParkingSlot(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    slot_no=models.CharField(max_length=10,default="")
    address=models.CharField(max_length=255,default="")
    direction_guidance=models.CharField(max_length=255,default="")
    slot_creator=models.ForeignKey(ParkingOwner,on_delete=models.CASCADE,related_name='slot_creator')
    slot_booking_qr=models.TextField(default="")
    is_active=models.BooleanField(default=True)
    is_suspended=models.BooleanField(default=False)
    created_at=models.DateTimeField(default=datetime.now())

    objects = ActiveManager()
    admin_objects = AdminManager() 

class ParkingSlotOpenCloseTime(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    slot=models.ForeignKey(ParkingSlot,on_delete=models.CASCADE,related_name='parking_slots_timings')
    day=models.CharField(max_length=20)
    open_time=models.TimeField(default=None)
    close_time=models.TimeField(default=None)
    is_active=models.BooleanField(default=True)

    objects = ActiveManager()
    admin_objects = AdminManager() 

class ParkingAreaOpenCloseTime(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    area=models.ForeignKey(ParkingArea,on_delete=models.CASCADE,related_name='parking_area_timings')
    day=models.CharField(max_length=20)
    open_time=models.TimeField(default=None)
    close_time=models.TimeField(default=None)
    is_active=models.BooleanField(default=True)

    objects = ActiveManager()
    admin_objects = AdminManager()

class ParkingSlotWithFacilities(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    parking_slot=models.ForeignKey(ParkingSlot,on_delete=models.CASCADE,related_name='parking_slots')
    facility=models.ForeignKey(SlotFacility,on_delete=models.CASCADE,related_name='parking_slot_facility',null=True)
    assigned_at=models.DateTimeField(default=datetime.now())
    is_active=models.BooleanField(default=True)

    objects = ActiveManager()
    admin_objects = AdminManager() 

class SlotUnderParkingArea(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    area=models.ForeignKey(ParkingArea,on_delete=models.CASCADE,related_name='parking_areas')
    slot=models.ForeignKey(ParkingSlot,on_delete=models.CASCADE,related_name='slot_under_parking_area')
    assigned_at=models.DateTimeField(default=datetime.now())
    is_verified=models.BooleanField(default=False)
    approved_by=models.ForeignKey(Admin,on_delete=models.SET_NULL,null=True,related_name='slot_approved_by')
    is_active=models.BooleanField(default=True)

    objects = ActiveManager()
    admin_objects = AdminManager() 

class Car(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    owner_name=models.CharField(max_length=100)
    owner_email=models.EmailField(max_length=100,unique=True)
    owner_phone=models.CharField(max_length=10,unique=True,null=True,blank=True)
    car_no=models.CharField(max_length=50,unique=True)
    car_pic=models.CharField(max_length=255,default="")
    owner_pic=models.CharField(max_length=255,default="")
    is_active=models.BooleanField(default=True)

    objects = ActiveManager()
    admin_objects = AdminManager() 

    def save(self, *args, **kwargs):
        self.name=self.name.upper()
        self.email=self.email.lower()
        super(Car, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name

class ArrivalDepart(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    car=models.ForeignKey(Car,on_delete=models.CASCADE,related_name='arrivaldept_car')
    parking_slot=models.ForeignKey(ParkingSlot,on_delete=models.CASCADE,related_name='arrivaldept_under_slot',default="")
    area=models.ForeignKey(ParkingArea,on_delete=models.CASCADE,related_name='arrivaldept_under_area',default="")
    arrival_time=models.DateTimeField(default=datetime.now())
    release_code=models.CharField(max_length=8)
    expected_depart_time=models.DateTimeField(default=None)
    actual_depart_time=models.DateTimeField(default=None)
    actual_charge=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    collected_charge=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    released_by_admin=models.ForeignKey(Admin,on_delete=models.SET_NULL,null=True,related_name='releasedby_admin')
    released_by_subadmin=models.ForeignKey(SubAdmin,on_delete=models.SET_NULL,null=True,related_name='releasedby_subadmin')
    released_by_parkingowner=models.ForeignKey(ParkingOwner,on_delete=models.SET_NULL,null=True,related_name='releasedby_parkingowner')
    is_active=models.BooleanField(default=True)

    objects = ActiveManager()
    admin_objects = AdminManager() 

class AdminChangingHistoryParkingAreas(models.Model):
    uid=models.CharField(max_length=100,unique=True)
    prev_admin=models.ForeignKey(Admin,on_delete=models.CASCADE,related_name='prev_changed_admin')
    current_admin=models.ForeignKey(Admin,on_delete=models.CASCADE,related_name='current_admin')
    parking_area=models.ForeignKey(ParkingArea,on_delete=models.CASCADE,related_name='parkingarea_adminhistory')
    changed_by=models.ForeignKey(SuperAdmin,on_delete=models.CASCADE,related_name='changing_approval_by')
    assigned_at=models.DateTimeField(default=datetime.now())
    is_active=models.BooleanField(default=True)

    objects = ActiveManager()
    admin_objects = AdminManager() 

class OTP(models.Model):
    user_id=models.CharField(max_length=100,unique=True)
    otp=models.CharField(max_length=6)
    created_at=models.DateTimeField(default=datetime.now())
    will_expire_at=models.DateTimeField(default=datetime.now())
    is_active=models.BooleanField(default=True)

    objects = ActiveManager()
    admin_objects = AdminManager() 

class TwoFactorVerification(models.Model):
    user_id=models.CharField(max_length=100,unique=True)
    qr_path=models.CharField(max_length=100)
    created_at=models.DateTimeField(default=datetime.now())
    is_active=models.BooleanField(default=True)

    objects = ActiveManager()
    admin_objects = AdminManager() 

class CountryCode(models.Model):
    country=models.CharField(max_length=100,unique=True)
    country_code=models.CharField(max_length=50)
    iso_code=models.CharField(max_length=100,unique=True)
    is_active=models.BooleanField(default=True)

    objects = ActiveManager()
    admin_objects = AdminManager() 

class EmailVerifyLinkSession(models.Model):
    user_id=models.CharField(max_length=100)
    link=models.TextField()
    created_at=models.DateTimeField(default=datetime.now())
    will_expire_at=models.DateTimeField(null=True,blank=True)

class CdnFileManager(models.Model):
    filename=models.CharField(max_length=100,unique=True)
    query_id=models.CharField(max_length=100,null=True)
    url=models.CharField(max_length=100,unique=True)
    public_id=models.CharField(max_length=100)
    asset_id=models.CharField(max_length=100)
    resource_type=models.CharField(max_length=100)
    folder=models.CharField(max_length=100)
    types=models.CharField(max_length=100)
    created_at=models.DateTimeField(default=datetime.now())
    
class ErrorLog(models.Model):
    uid = models.CharField(max_length=100, primary_key=True)
    error_message=models.TextField()
    user_id=models.CharField(max_length=100,null=True,blank=True)
    user_type=models.CharField(max_length=100,null=True,blank=True)
    request_method=models.CharField(max_length=100,null=True,blank=True)
    request_headers=models.TextField(null=True,blank=True)
    request_parameters=models.CharField(max_length=100,null=True,blank=True)
    request_body=models.TextField(null=True,blank=True)
    client_ip=models.CharField(max_length=100,null=True,blank=True)
    stack_trace=models.TextField()
    exception_type=models.CharField(max_length=100,null=True,blank=True)
    view_name=models.CharField(max_length=100,null=True,blank=True)
    response_status_code=models.CharField(max_length=100,null=True,blank=True)
    enviroment=models.CharField(max_length=100,null=True,blank=True)
    error_location=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateTimeField(default=datetime.now())
    
    def __str__(self) -> str:
        return f"Error : {self.response_status_code} at {self.created_at}"

class AccessLog(models.Model):
    uid = models.CharField(max_length=100, primary_key=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(max_length=255, null=True, blank=True)
    request_method = models.CharField(max_length=255, null=True, blank=True)
    request_headers = models.TextField(null=True, blank=True)
    request_parameters = models.CharField(max_length=255, null=True, blank=True)
    request_body = models.TextField(null=True, blank=True)
    client_ip = models.CharField(max_length=255, null=True, blank=True)
    view_name = models.CharField(max_length=255, null=True, blank=True)
    response_status_code = models.CharField(max_length=255, null=True, blank=True)
    environment = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now())
    response_content = models.TextField(null=True, blank=True)
    request_url = models.URLField(max_length=2000, null=True, blank=True)
    user_agent = models.CharField(max_length=1000, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    referer = models.URLField(max_length=2000, null=True, blank=True)
    request_query_params = models.JSONField(null=True, blank=True)
    response_headers = models.TextField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f"Log: {self.response_status_code} at {self.created_at} method {self.request_method} url {self.request_url}"
