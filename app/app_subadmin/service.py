from django.shortcuts import render,redirect
from django.http import JsonResponse,Http404,HttpResponse,HttpResponseRedirect, HttpResponsePermanentRedirect
from utils.jwt_builder import JwtBuilder
from app.models import Admin,SubAdmin,ParkingArea,Role,SubAdminUnderParkingArea
import json
from utils.id_generator import generate_unique_id
from utils.emails import SendMail
from decouple import config
from multiprocessing import Process
from django.db import transaction

def login(email:str,password:str)->JsonResponse:
    try:
        jwt_builder = JwtBuilder()
        try:
            subadmin = SubAdmin.objects.get(email=email)
        except SubAdmin.DoesNotExist:
            return JsonResponse({"message": "User doesn't exist!","status":400}, status=400)
        if not subadmin.is_correct_password(password):
            return JsonResponse({"message": "Wrong password!","status":400}, status=400)
        if subadmin.is_suspended:
            return JsonResponse({"message": "You are suspended right now!","status":400}, status=400)
        
        if not subadmin.is_verified:
            return JsonResponse({"message": "You are not verified yet!","status":400}, status=400)
        payload = {"user_id": subadmin.uid, "role": subadmin.role.role_name,"sub":subadmin.name}
        tokens = jwt_builder.get_token(payload)
        response = JsonResponse({"message": "Login successful","status":200},status=200)
        response.set_cookie('access_token', tokens['access_token'], httponly=True, secure=True)
        response.set_cookie('refresh_token', tokens['refresh_token'], httponly=True, secure=True)
        return response
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON","status":400}, status=400)
    except Exception as e:
        return JsonResponse({"message": "Something is wrong","status":500}, status=500)


def register(admin_id:str,name:str,email:str,phone:str,password:str,parking_area_ids:list[str],role:Role)->HttpResponseRedirect | HttpResponsePermanentRedirect|JsonResponse:
    try:
        uid=generate_unique_id()
        admin=Admin.objects.get(uid=admin_id)
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
            args=('Registered Successfully!',f'Hello {name} Your Account has been created as {role.ui_name}.\nYour UserId is {email} and Password is {password}.\nYour Account will be activated shortly and we will inform you!',email)
        )
        p.start()
        return redirect('/sub-admin/login')
    except Exception as e:
        return JsonResponse({"message":"something is wrong!","status":500},status=500)