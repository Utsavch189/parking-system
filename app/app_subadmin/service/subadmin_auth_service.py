from typing import Tuple
from utils.jwt_builder import JwtBuilder
from app.models import Admin,SubAdmin,ParkingArea,Role,SubAdminUnderParkingArea
import json
from utils.id_generator import generate_unique_id
from utils.emails import SendMail
from decouple import config
from multiprocessing import Process
from django.db import transaction
from utils.string import StringBuilder


def login(email:str,password:str)->Tuple[dict,int]:
    try:
        email=StringBuilder(email).normalize_spaces().trim_string().build()
        password=StringBuilder(password).normalize_spaces().trim_string().build()

        jwt_builder = JwtBuilder()

        try:
            subadmin = SubAdmin.objects.get(email=email)
        except SubAdmin.DoesNotExist:
            return {"message": "User doesn't exist!","status":400}, 400
        if not subadmin.is_correct_password(password):
            return {"message": "Wrong password!","status":400}, 400
        if subadmin.is_suspended:
            return {"message": "You are suspended right now!","status":400}, 400
        if not subadmin.is_verified:
            return {"message": "You are not verified yet!","status":400}, 400
        
        payload = {"user_id": subadmin.uid, "role": subadmin.role.role_name,"sub":subadmin.name}
        tokens = jwt_builder.get_token(payload)
        return tokens,200
    except json.JSONDecodeError:
        return {"message": "Invalid JSON","status":400}, 400
    except Exception as e:
        return {"message": "Something is wrong","status":500}, 500


def register(admin_id:str,name:str,email:str,phone:str,password:str,parking_area_ids:list[str])->Tuple[bool,dict,int]:
    try:
        uid=generate_unique_id()
        admin=Admin.objects.get(uid=admin_id)
        role=Role.objects.get(role_name='SUBADMIN')
        with transaction.atomic():
            sub_admin=SubAdmin(
                uid=uid,
                name=name,
                email=email,
                phone=phone,
                password=password,
                pincode=admin.pincode,
                country_code=admin.country_code,
                associate_admin=admin,
                role=role
            )
            sub_admin.save()
            for area_id in parking_area_ids:
                parking_area=ParkingArea.objects.get(uid=area_id)
                sub_admin_associate_area=SubAdminUnderParkingArea(
                    uid=generate_unique_id(),
                    sub_admin=sub_admin,
                    admin=admin,
                    parking_area=parking_area
                )
                sub_admin_associate_area.save()
        p=Process(
            target=SendMail.send_email,
            args=('Registered Successfully!',f'Hello {name} Your Account has been created as {role.ui_name}.\nYour UserId is {email} and Password is {password}.\nYour Account will be verified shortly and we will inform you!',email)
        )
        p.start()
        return True,{},201
    except Exception as e:
        return False,{"message":"something is wrong!","status":500},500