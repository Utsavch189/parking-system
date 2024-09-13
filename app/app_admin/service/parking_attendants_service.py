from typing import Tuple
from app.models import SubAdmin,Admin,EmailVerifyLinkSession
from utils.emails import SendMail
from app.serializers.sub_admin import SubAdminSerializer
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from datetime import datetime,timedelta
from multiprocessing import Process
from decouple import config
from utils.encrypt import encrypt,decrypt
from django.utils import timezone

BASE_URL=config('BASE_URL')
APP_NAME=config('APP_NAME')

def get_all_attendants(page:int,page_size:int,user_id:str)->Tuple[dict,int]:
    try:
        attached_subadmins=SubAdmin.objects.filter(associate_admin__uid=user_id).order_by('-created_at')
        total_records=attached_subadmins.count()
        paginator=Paginator(attached_subadmins,int(page_size))
        try:
            attached_subadmin=paginator.page(int(page))
        except PageNotAnInteger:
            attached_subadmin=paginator.page(1)
        except EmptyPage:
            attached_subadmin=[]
        attached_subadmins=SubAdminSerializer(attached_subadmin,many=True).data
        return {"attached_subadmins":attached_subadmins,"total_records":total_records,"status":200},200
    except Exception as e:
        return {"message":"something is wrong!","status":500},500

def attendant_delete_confirmation_mail(user_id:str,attendant_id:str)->Tuple[dict,int]:
    try:
        admin=Admin.objects.get(uid=user_id)
        parking_attendant=SubAdmin.objects.get(uid=attendant_id)
        delete_link=f"{BASE_URL}/admins/delete-confirm-attendant/{encrypt(user_id)}&{encrypt(parking_attendant.uid)}"
        subject=f"Hello {admin.name} do you want to delete parking attendant {parking_attendant.name} ?"
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
        return {"message":"something is wrong!","status":500},500
    
def attendant_actual_delete(user_id:str,attendant_id:str)->Tuple[bool,dict]:
    delete_link=f"{BASE_URL}/admins/delete-confirm-attendant/{admin_id}&{attendant_id}"
    admin_id=decrypt(user_id)
    attendant_id=decrypt(attendant_id)
    try:
        parking_attendant=SubAdmin.objects.get(uid=attendant_id)
    except SubAdmin.DoesNotExist:
        return False,{}
    if not EmailVerifyLinkSession.objects.filter(user_id=admin_id,link=delete_link).exists():
        return False,{}
    link_session=EmailVerifyLinkSession.objects.filter(user_id=admin_id,link=delete_link)[0]
    if link_session.will_expire_at<timezone.now():
        link_session.delete()
        return False,{}
    link_session.delete()
    context={
        "title":f"Delete Confirmation for Parking Attendant {parking_attendant.name}",
        "name":f"Parking Attendant {parking_attendant.name}"
    }
    parking_attendant.is_active=False
    parking_attendant.save()
    return True,context

def attendant_verify_toggle(attendant_id:str)->Tuple[dict,int]:
    try:
        try:
            parking_attendant=SubAdmin.objects.get(uid=attendant_id)
        except SubAdmin.DoesNotExist:
            return {"message":"user not found!","status":400},400
            
        if parking_attendant.is_verified:
            message=f"{parking_attendant.name} is now unverified!"
            email_subject=f"Hello {parking_attendant.name} from {APP_NAME}"
            email_body=f"{parking_attendant.name} Your Account is now UnVerified!\nFor any information connect with your Area Manager."
            parking_attendant.is_verified=False
        else:
            message=f"{parking_attendant.name} is now verified!"
            email_subject=f"Hello {parking_attendant.name} from {APP_NAME}"
            email_body=f"{parking_attendant.name} Your Account is now Verified and you can login!\nFor any information connect with your Area Manager.\nClick the link to login.\n{config('BASE_URL')}/sub-admin/login"
            parking_attendant.is_verified=True
        
        parking_attendant.save()
        p=Process(
            target=SendMail.send_email,
            args=(
                email_subject,
                email_body,
                parking_attendant.email
            )
        )
        p.start()
        return {"message":message,"status":200},200
    except Exception as e:
        return {"message":"something is wrong!","status":500},500
    
def attendant_suspend_toggle(attendant_id:str)->Tuple[dict,int]:
    try:
        try:
            parking_attendant=SubAdmin.objects.get(uid=attendant_id)
        except SubAdmin.DoesNotExist:
            return {"message":"user not found!","status":400},400
        
        if parking_attendant.is_suspended:
            message=f"{parking_attendant.name} is now unsuspended!"
            email_subject=f"Hello {parking_attendant.name} from {APP_NAME}"
            email_body=f"{parking_attendant.name} Your Account is now UnSuspended and you can login!\nFor any information connect with your Area Manager.\nClick the link to login.\n{config('BASE_URL')}/sub-admin/login"
            parking_attendant.is_verified=False
        else:
            message=f"{parking_attendant.name} is now suspended!"
            email_subject=f"Hello {parking_attendant.name} from {APP_NAME}"
            email_body=f"{parking_attendant.name} Your Account is now Suspended!\nFor any information connect with your Area Manager."
            parking_attendant.is_verified=True
        
        parking_attendant.save()
        p=Process(
            target=SendMail.send_email,
            args=(
                email_subject,
                email_body,
                parking_attendant.email
            )
        )
        p.start()
        return {"message":message,"status":200},200
    except Exception as e:
        return {"message":"something is wrong!","status":500},500