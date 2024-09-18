from typing import Tuple
from utils.jwt_builder import JwtBuilder
import json
from app.models import Admin,ParkingOwner,Role,CountryCode
from utils.id_generator import generate_unique_id
from utils.emails import SendMail
from multiprocessing import Process
from django.db import transaction
from utils.string import StringBuilder

def login(email:str,password:str)->Tuple[dict,int]:
    try:
        email=StringBuilder(email).normalize_spaces().trim_string().build()
        password=StringBuilder(password).normalize_spaces().trim_string().build()

        jwt_builder = JwtBuilder()

        try:
            parking_owner = ParkingOwner.objects.get(email=email)
        except ParkingOwner.DoesNotExist:
            return {"message": "User doesn't exist!","status":400}, 400
        if not parking_owner.is_correct_password(password):
            return {"message": "Wrong password!","status":400}, 400
        if parking_owner.is_suspended:
            return {"message": "You are suspended right now!","status":400}, 400
        if not parking_owner.is_verified:
            return {"message": "You are not verified yet!","status":400}, 400
        
        payload = {"user_id": parking_owner.uid, "role": parking_owner.role.role_name,"sub":parking_owner.name}
        tokens = jwt_builder.get_token(payload)
        return tokens,200
    except json.JSONDecodeError:
        return {"message": "Invalid JSON","status":400}, 400
    except Exception as e:
        return {"message": "Something is wrong","status":500}, 500


def register(name:str,email:str,phone:str,password:str,pincode:str,country:str)->Tuple[bool,dict,int]:
    try:
        uid=generate_unique_id()
        role=Role.objects.get(role_name='PARKINOWNER')
        country_code=CountryCode.objects.get(country=country).country_code
        parking_owner=ParkingOwner(
            uid=uid,
            name=name,
            email=email,
            phone=phone,
            password=password,
            pincode=pincode,
            country_code=country_code,
            role=role,
            is_verified=True
        )
        parking_owner.save()
        p=Process(
            target=SendMail.send_email,
            args=('Registered Successfully!',f'Hello {name} Your Account has been created as {role.ui_name}.\nYour UserId is {email} and Password is {password}.',email)
        )
        p.start()
        return True,{"message":"account is created!","status":201},201
    except Exception as e:
        return False,{"message":"something is wrong!","status":500},500