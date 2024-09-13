from utils.jwt_builder import JwtBuilder
from utils.string import StringBuilder
from app.models import Admin,CdnFileManager,CountryCode,Role
from typing import Tuple
import json
from utils.id_generator import generate_unique_id
from utils.encrypt import encrypt
from django.db import transaction
from multiprocessing import Process
from utils.qr import get_qr
import random
from utils.cdn import CDN
from decouple import config
from utils.emails import SendMail

BASE_URL=config('BASE_URL')
CDN=CDN()

def login(email:str,password:str)->Tuple[dict,int]:
    try:
        email=StringBuilder(email).normalize_spaces().trim_string().build()
        password=StringBuilder(password).normalize_spaces().trim_string().build()
        jwt_builder = JwtBuilder()

        try:
            admin = Admin.objects.get(email=email)
        except Admin.DoesNotExist:
            return {"message":"User doesn't exist!","status":400},400
        
        if not admin.is_correct_password(password):
            return {"message":"Wrong password!","status":400},400
        
        if admin.is_suspended:
            return {"message":"You are suspended right now!","status":400},400
        
        if not admin.is_verified:
            return {"message":"You are not verified yet!","status":400},400
        
        payload = {"user_id": admin.uid, "role": admin.role.role_name,"sub":admin.name}
        tokens = jwt_builder.get_token(payload)
        return tokens,200
    
    except json.JSONDecodeError as error:
        return {"message": "Invalid JSON","status":400},400
    
    except Exception as e:
        return {"message": "Something is wrong","status":500},500
    

def register(name:str,email:str,phone:str,password:str,pincode:str,country:str)->Tuple[bool,dict,int]:
    try:
        name=StringBuilder(name).normalize_spaces().trim_string().build()
        email=StringBuilder(email).normalize_spaces().trim_string().build()
        phone=StringBuilder(phone).normalize_spaces().trim_string().build()
        password=StringBuilder(password).normalize_spaces().trim_string().build()
        pincode=StringBuilder(pincode).normalize_spaces().trim_string().build()
        country=StringBuilder(country).normalize_spaces().trim_string().build()
        
        country_code=CountryCode.objects.get(country=country).country_code
        admin_id=generate_unique_id()

        # create subadmin register qr
        subadmin_register_qr_filename=f"{admin_id}_{generate_unique_id()+str(random.randint(1111,9999))}"
        subadmin_register_qr_dest=f'parking_system/areavolentier_registerqr/{subadmin_register_qr_filename}'
        subadmin_register_qr_url=f"{BASE_URL}/sub-admin/register/{encrypt(admin_id)}"
        subadmin_register_qr=get_qr(subadmin_register_qr_url)
        subadmin_register_qr_res=CDN.upload(source=subadmin_register_qr,destination=subadmin_register_qr_dest)
    
        role=Role.objects.get(role_name='ADMIN')

        with transaction.atomic():
            admin=Admin(
                uid=admin_id,
                name=name,
                email=email,
                phone=phone,
                password=password,
                pincode=pincode,
                country_code=country_code,
                role=role,
                subadmin_register_qr=subadmin_register_qr_res.get('secure_url')
            )
            admin.save()

            subadmin_register_qr_cdnmanager=CdnFileManager(
                filename=subadmin_register_qr_filename,
                query_id='SUBADMIN_REG'+admin_id,
                url=subadmin_register_qr_res.get('secure_url'),
                public_id=subadmin_register_qr_res.get('public_id'),
                asset_id=subadmin_register_qr_res.get('asset_id'),
                resource_type=subadmin_register_qr_res.get('resource_type'),
                folder=subadmin_register_qr_res.get('folder'),
                types=subadmin_register_qr_res.get('type')
            )
            subadmin_register_qr_cdnmanager.save()
        
        p=Process(
            target=SendMail.send_email,
            args=('Registered Successfully!',f'Hello {name} Your Account has been created as {role.ui_name}.\nYour UserId is {email} and Password is {password}.\nYour Account will be activated shortly and we will inform you!',email)
        )
        p.start()
        return True,{},201
    except Exception as e:
        return False,{"message":"something is wrong!","status":500},500