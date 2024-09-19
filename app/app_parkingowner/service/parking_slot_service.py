from app.models import SlotFacility,ParkingOwner,ParkingSlot,ParkingSlotOpenCloseTime,ParkingSlotWithFacilities
from utils.id_generator import generate_unique_id
from django.db import transaction
from typing import Tuple
import time
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from app.serializers.slots import ParkingSlotSerializer

def create_slot(user_id:str,slot_address:str,slot_direction_guidance:str,facilities:list,timings:list)->Tuple[dict,int]:
    try:
        try:
            parking_owner=ParkingOwner.objects.get(uid=user_id)
        except ParkingOwner.DoesNotExist:
            return {"message":"user not found!","status":400},400
        
        slot_no=int(time.time()) % 1000000
        slot_id=generate_unique_id()

        with transaction.atomic():
            
            slot=ParkingSlot(
                uid=slot_id,
                slot_no=slot_no,
                address=slot_address,
                direction_guidance=slot_direction_guidance,
                slot_creator=parking_owner,
                slot_booking_qr="N/A",
            )
            slot.save()

            for t in timings:
                timing=ParkingSlotOpenCloseTime(
                    uid=generate_unique_id(),
                    slot=slot,
                    day=t.get('day'),
                    open_time=t.get('open_time'),
                    close_time=t.get('close_time')
                )
                timing.save()
            
            for f in facilities:
                facility=ParkingSlotWithFacilities(
                    uid=generate_unique_id(),
                    parking_slot=slot,
                    facility=SlotFacility.objects.get(uid=f.get('uid'))
                )
                facility.save()
            
        return {"message":"new slot is created","status":201},201
    except Exception as e:
        print(e)
        return {"message":"something is wrong!","status":500},500
    
def get_slots(page:int,page_size:int,user_id:str)->Tuple[dict,int]:
    try:
        slots=ParkingSlot.objects.filter(slot_creator__uid=user_id)
        total_records=slots.count()
        paginator=Paginator(slots,int(page_size))
        try:
            slot=paginator.page(int(page))
        except PageNotAnInteger:
            slot=paginator.page(1)
        except EmptyPage:
            slot=[]
        slots=ParkingSlotSerializer(slot,many=True).data
        return {"slots":slots,"total_records":total_records,"status":200},200
    except Exception as e:
        return {"message":"something is wrong!","status":500},500