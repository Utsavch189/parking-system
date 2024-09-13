from typing import Tuple
from utils.string import StringBuilder
from app.models import (Admin,ParkingArea,CdnFileManager,
                        SlotFacility,FacilityChargesForArea,
                        ParkingAreaOpenCloseTime,EmailVerifyLinkSession)
from utils.id_generator import generate_unique_id
from multiprocessing import Process
from django.db import transaction
from utils.qr import get_qr
import random
from utils.cdn import CDN
from decouple import config
from utils.encrypt import encrypt,decrypt
from datetime import datetime,timedelta
from utils.emails import SendMail
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from app.serializers.parking_areas import ParkingAreaSerializer
from django.utils import timezone

BASE_URL=config('BASE_URL')
CDN=CDN()

def create_parking_area(user_id:str,area_name:str="",facilities:list[dict]=[],selected_days:list[dict]=[])->Tuple[dict,int]:
    try:
        area_name=StringBuilder(area_name).normalize_spaces().trim_string().build()
        admin=Admin.objects.get(uid=user_id)

        if area_name and not facilities and not selected_days:
            # validate area name
            if ParkingArea.objects.filter(admin__pincode=admin.pincode,admin__country_code=admin.country_code,area_name=area_name).exists():
                return {"message":"area name already in use!","status":400},400
            return {"message":"area name is fine!","status":200},200

        elif area_name and facilities and selected_days:
            # create area
            parking_area_id=generate_unique_id()

            # parking_owner_register_qr making
            parking_owner_register_qr_filename=f"{user_id}_{generate_unique_id()+str(random.randint(1111,9999))}"
            parking_owner_register_qr_dest=f'parking_system/parkingowner_registerqr/{parking_owner_register_qr_filename}'
            parking_owner_register_qr_url=f"{BASE_URL}/parking-owner/register/{encrypt(parking_area_id)}&{encrypt(user_id)}"
            parking_owner_register_qr=get_qr(parking_owner_register_qr_url)
            parking_owner_register_res=CDN.upload(source=parking_owner_register_qr,destination=parking_owner_register_qr_dest)

            # searchingslots_qr making
            searchingslots_qr_filename=f"{user_id}_{generate_unique_id()+str(random.randint(1111,9999))}"
            searchingslots_qr_dest=f'parking_system/slotsearching_qr/{searchingslots_qr_filename}'
            searchingslots_qr_url=f"{BASE_URL}/users/slot-search/{encrypt(parking_area_id)}&{encrypt(user_id)}"
            searchingslots_qr=get_qr(searchingslots_qr_url)
            searchingslots_res=CDN.upload(source=searchingslots_qr,destination=searchingslots_qr_dest)

            with transaction.atomic():
                parking_area=ParkingArea(
                    uid=parking_area_id,
                    area_name=area_name,
                    parking_owner_register_qr=parking_owner_register_res.get('secure_url'),
                    searchingslots_qr=searchingslots_res.get('secure_url'),
                    admin=admin
                )
                parking_area.save()

                parking_owner_register_qr_cdnmanager=CdnFileManager(
                    filename=parking_owner_register_qr_filename,
                    query_id=parking_area_id,
                    url=parking_owner_register_res.get('secure_url'),
                    public_id=parking_owner_register_res.get('public_id'),
                    asset_id=parking_owner_register_res.get('asset_id'),
                    resource_type=parking_owner_register_res.get('resource_type'),
                    folder=parking_owner_register_res.get('folder'),
                    types=parking_owner_register_res.get('type')
                )
                parking_owner_register_qr_cdnmanager.save()

                searchingslot_qr_cdnmanager=CdnFileManager(
                    filename=searchingslots_qr_filename,
                    query_id=parking_area_id,
                    url=searchingslots_res.get('secure_url'),
                    public_id=searchingslots_res.get('public_id'),
                    asset_id=searchingslots_res.get('asset_id'),
                    resource_type=parking_owner_register_res.get('resource_type'),
                    folder=searchingslots_res.get('folder'),
                    types=searchingslots_res.get('type')
                )
                searchingslot_qr_cdnmanager.save()

                for facility in facilities:
                    facilities_for_parking_area=FacilityChargesForArea(
                        uid=generate_unique_id(),
                        charges=facility.get('charges'),
                        penalty_charge_per_hour=facility.get('penalty_charge_per_hour'),
                        facility=SlotFacility.objects.get(uid=facility.get('id')),
                        area=parking_area
                    )
                    facilities_for_parking_area.save()
                
                for timing in selected_days:
                    timings=ParkingAreaOpenCloseTime(
                        uid=generate_unique_id(),
                        area=parking_area,
                        day=timing.get('day'),
                        open_time=timing.get('open_time'),
                        close_time=timing.get('close_time'),
                    )
                    timings.save()
            return {"message":"created!","status":201},201
        else:
            return {"message":"bad request!","status":400},400
    except Exception as e:
        return {"message":"something is wrong!","status":500},500
    
def update_parking_area(user_id:str,area_id:str,area_name:str="",facilities:list[dict]=[],selected_days:list[dict]=[])->Tuple[dict,int]:
    try:
        area_id=StringBuilder(area_id).normalize_spaces().trim_string().build()
        admin=Admin.objects.get(uid=user_id)

        try:
            parking_area=ParkingArea.objects.get(uid=area_id)
        except ParkingArea.DoesNotExist:
            return {"message":"area not found!","status":400},400

        # update area name
        if area_name and area_id and not facilities and not selected_days:
            area_name=StringBuilder(area_name).normalize_spaces().trim_string().build()
            if ParkingArea.objects.filter(admin__pincode=admin.pincode,admin__country_code=admin.country_code,area_name=area_name).exists():
                return {"message":"area name already in use!","status":400},400
            parking_area.area_name=area_name
            parking_area.save()
            return {"message":"area name is updated!","status":200},200

        # update facilities
        elif facilities and area_id and not area_name and not selected_days:

            prev_facilities=[i.facility.uid for i in FacilityChargesForArea.objects.filter(area__uid=area_id)]
            incoming_facilities=[i.get('id') for i in facilities]
            missing_facilities=list(set(prev_facilities)-set(incoming_facilities))
            
            for facility_id in missing_facilities:
                existing_facility=FacilityChargesForArea.objects.filter(area__uid=area_id,facility__uid=facility_id)[0]
                existing_facility.delete()
            
            for facility in facilities:
                existing_facility=FacilityChargesForArea.objects.filter(area__uid=area_id,facility__uid=facility.get('id'))
                if existing_facility.exists():
                    existing_facility_obj=existing_facility[0]
                    existing_facility_obj.charges=facility.get('charges')
                    existing_facility_obj.penalty_charge_per_hour=facility.get('penalty_charge_per_hour')
                    existing_facility_obj.updated_at=datetime.now()
                    existing_facility_obj.last_updated_by=admin
                    existing_facility_obj.save()
                else:
                    facilities_for_parking_area=FacilityChargesForArea(
                        uid=generate_unique_id(),
                        charges=facility.get('charges'),
                        penalty_charge_per_hour=facility.get('penalty_charge_per_hour'),
                        facility=SlotFacility.objects.get(uid=facility.get('id')),
                        area=parking_area
                    )
                    facilities_for_parking_area.save()
            return {"message":"area facilities are updated!","status":200},200
        
        # update timings
        elif selected_days and area_id and not area_name and not facilities:

            prev_days=[i.day for i in ParkingAreaOpenCloseTime.objects.filter(area__uid=area_id)]
            incoming_days=[i.get('day') for i in selected_days]
            missing_days=list(set(prev_days)-set(incoming_days))
            
            for day in missing_days:
                existing_timing=ParkingAreaOpenCloseTime.objects.filter(area__uid=area_id,day=day)[0]
                existing_timing.delete()
            
            for timing in selected_days:
                existing_timing=ParkingAreaOpenCloseTime.objects.filter(area__uid=area_id,day=timing.get('day'))
                if existing_timing.exists():
                    existing_timing_obj=existing_timing[0]
                    existing_timing_obj.open_time=timing.get('open_time')
                    existing_timing_obj.close_time=timing.get('close_time')
                    existing_timing_obj.save()
                else:
                    timings=ParkingAreaOpenCloseTime(
                        uid=generate_unique_id(),
                        area=parking_area,
                        day=timing.get('day'),
                        open_time=timing.get('open_time'),
                        close_time=timing.get('close_time'),
                    )
                    timings.save()
            return {"message":"area timings are updated!","status":200},200
        
        else:
            return {"message":"bad request!","status":400},400
    
    except Exception as e:
        print(f"Error.......... {e}")
        return {"message":"something is wrong!","status":500},500
    
def get_all_parking_areas(page:int,page_size:int,user_id:str)->Tuple[dict,int]:
    try:
        areas=ParkingArea.objects.filter(admin__uid=user_id).order_by('-created_at')
        total_records=areas.count()
        paginator=Paginator(areas,int(page_size))
        try:
            area=paginator.page(int(page))
        except PageNotAnInteger:
            area=paginator.page(1)
        except EmptyPage:
            area=[]
        areas=ParkingAreaSerializer(area,many=True).data
        return {"areas":areas,"total_records":total_records,"status":200},200
    except Exception as e:
        return {"message":"something is wrong!","status":500},500
    
def parkingarea_delete_confirmation_mail(user_id:str,area_id:str)->Tuple[dict,int]:
    try:
        admin=Admin.objects.get(uid=user_id)
        parking_area=ParkingArea.objects.get(uid=area_id)
        delete_link=f"{BASE_URL}/admins/delete-confirm-area/{encrypt(user_id)}&{encrypt(parking_area.uid)}"
        subject=f"Hello {admin.name} do you want to delete area {parking_area.area_name} ?"
        body=f" Link will be valid for 3 minutes. \n Press the link to delete it ! \n {delete_link}"
        EmailVerifyLinkSession.objects.create(
            user_id=user_id,
            link=delete_link,
            will_expire_at=datetime.now()+timedelta(minutes=3)
        )
        p=Process(
            target=SendMail.send_email,
            args=(
                subject,
                body,
                admin.email
            )
        )
        p.start()
        return {"message":"confirmation link is sent to your email!","status":200},200
    except Exception as e:
        print(f"ERRoR............. {e}")
        return {"message":"something is wrong!","status":500},500
    
def parkingarea_actual_delete(user_id:str,area_id:str)->Tuple[bool,dict]:
    delete_link=f"{config('BASE_URL')}/admins/delete-confirm-area/{admin_id}&{area_id}"
    admin_id=decrypt(user_id)
    area_id=decrypt(area_id)
    try:
        parking_area=ParkingArea.objects.get(uid=area_id)
    except ParkingArea.DoesNotExist:
        return False,{}
    if not EmailVerifyLinkSession.objects.filter(user_id=admin_id,link=delete_link).exists():
        return False,{}
    link_session=EmailVerifyLinkSession.objects.filter(user_id=admin_id,link=delete_link)[0]
    if link_session.will_expire_at<timezone.now():
        link_session.delete()
        return False,{}
    link_session.delete()
    cdn_files=CdnFileManager.objects.filter(query_id=area_id)
    for file in cdn_files:
        CDN.delete(
            public_ids=file.public_id,
            resource_type=file.resource_type,
            type=file.types
        )
        file.delete()
    context={
        "title":f"Delete Confirmation for Area {parking_area.area_name}",
        "name":f"Area {parking_area.area_name}"
    }
    parking_area.is_active=False
    parking_area.save()
    return True,context
