from django.views import View
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from app.models import (Admin,ParkingArea,FacilityChargesForArea,
                        SlotFacility,ParkingAreaOpenCloseTime,
                        EmailVerifyLinkSession,CdnFileManager,CountryCode,
                        Role)
from utils.jwt_builder import JwtBuilder
from django.utils import timezone
from utils.decorators.login_requires import login_required
from django.http import JsonResponse,Http404,HttpResponse
from app.models import SlotFacility
from django.core.serializers import serialize
import json
from utils.string import StringBuilder
from utils.encrypt import encrypt,decrypt
from django.db import transaction
from utils.id_generator import generate_unique_id
from datetime import datetime,timedelta
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from app.app_admin.serializers.parking_areas import ParkingAreaSerializer
from utils.emails import SendMail
from decouple import config
from multiprocessing import Process
from utils.qr import get_qr
import random
from utils.cdn import CDN

CDN=CDN()

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):

    def get(self,request):
        print("user in login view",request._user)
        if request._user:
            return redirect('/admins')
        return render(request,'admins/login.html')
    
    def post(self,request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            email = data.get('email')
            password = data.get('password')
            jwt_builder = JwtBuilder()

            try:
                admin = Admin.objects.get(email=email)
            except Admin.DoesNotExist:
                return JsonResponse({"message": "User doesn't exist!","status":400}, status=400)

            if not admin.is_correct_password(password):
                return JsonResponse({"message": "Wrong password!","status":400}, status=400)

            if admin.is_suspended:
                return JsonResponse({"message": "You are suspended right now!","status":400}, status=400)

            payload = {"user_id": admin.uid, "role": admin.role.role_name}
            tokens = jwt_builder.get_token(payload)

            response = JsonResponse({"message": "Login successful","status":200},status=200)
            response.set_cookie('access_token', tokens['access_token'], httponly=True, secure=True)
            response.set_cookie('refresh_token', tokens['refresh_token'], httponly=True, secure=True)
            return response
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON","status":400}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Something is wrong","status":500}, status=500)


class HomeView(View):

    @login_required(login_url="/admins/login")
    def get(self,request):
        response=render(request,'admins/home.html')
        return response
    
class GetFacilities(View):

    @login_required(login_url="/admins/login",json_response=True)
    def get(self,request):
        try:
            facilities=SlotFacility.objects.all()
            data=serialize('json',facilities)
            return JsonResponse({"data":data},status=200)
        except Exception as e:
            return JsonResponse({"message":"something went wrong!","status":500},status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ParkingAreaView(View):

    @login_required(login_url="/admins/login",json_response=True)
    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        area_name=data.get('area_name',None)
        facilities=data.get('facilities',None)
        selected_days=data.get('selected_days',None)
        user_id=request._user.get('user_id')

        if area_name and not facilities and not selected_days:
            try:
                builder=StringBuilder(area_name)
                area_name=builder.normalize_spaces().trim_string().build()
                admin=Admin.objects.get(uid=user_id)
                if ParkingArea.objects.filter(admin__pincode=admin.pincode,admin__country_code=admin.country_code,area_name=area_name).exists():
                    return JsonResponse({"message":"area name already in use!","status":400},status=400)

                return JsonResponse({"message":"area name is fine!","status":200},status=200)
            except Exception as e:
                print(e)
                return JsonResponse({"message":"something is wrong!","status":500},status=500)

        elif area_name and facilities and selected_days:
            try:                
                builder=StringBuilder(area_name)
                area_name=builder.normalize_spaces().trim_string().build()
                admin=Admin.objects.get(uid=user_id)
                parking_area_id=generate_unique_id()
                # # parking_owner_register_qr making
                parking_owner_register_qr_filename=f"{user_id}_{generate_unique_id()+str(random.randint(1111,9999))}.png"
                parking_owner_register_qr_dest=f'parking_system/parkingowner_registerqr/{parking_owner_register_qr_filename}'
                parking_owner_register_qr_url=f"{config('BASE_URL')}/parking-owner/register/{encrypt(parking_area_id)}&{encrypt(user_id)}"
                parking_owner_register_qr=get_qr(parking_owner_register_qr_url)
                parking_owner_register_res=CDN.upload(source=parking_owner_register_qr,destination=parking_owner_register_qr_dest)
                # print(parking_owner_register_res)

                # # searchingslots_qr making
                searchingslots_qr_filename=f"{user_id}_{generate_unique_id()+str(random.randint(1111,9999))}.png"
                searchingslots_qr_dest=f'parking_system/slotsearching_qr/{searchingslots_qr_filename}'
                searchingslots_qr_url=f"{config('BASE_URL')}/users/slot-search/{encrypt(parking_area_id)}&{encrypt(user_id)}"
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

                return JsonResponse({"message":"created!","status":200},status=200)
            except Exception as e:
                print(e)
                return JsonResponse({"message":"something is wrong!","status":500},status=500)
        else:
            return JsonResponse({"message":"bad request!","status":400},status=400)
    
    @login_required(login_url="/admins/login",json_response=True)
    def put(self,request):
        data = json.loads(request.body.decode('utf-8'))
        area_id=data.get('area_id',None)
        area_name=data.get('area_name',None)
        _facilities=data.get('facilities',None)
        _selected_days=data.get('selected_days',None)
        user_id=request._user.get('user_id')
        admin=Admin.objects.get(uid=user_id)

        # update area name
        if area_name and area_id and not _facilities and not _selected_days:
            try:
                builder=StringBuilder(area_name)
                area_name=builder.normalize_spaces().trim_string().build()
                if ParkingArea.objects.filter(admin__pincode=admin.pincode,admin__country_code=admin.country_code,area_name=area_name).exists():
                    return JsonResponse({"message":"area name already in use!","status":400},status=400)

                try:
                    parking_area=ParkingArea.objects.get(uid=area_id)
                except ParkingArea.DoesNotExist:
                    return JsonResponse({"message":"area not found!","status":400},status=400)

                parking_area.area_name=area_name
                parking_area.save()

                return JsonResponse({"message":"area name is updated!","status":200},status=200)
            except Exception as e:
                print(e)
                return JsonResponse({"message":"something is wrong!","status":500},status=500)

        # update facilities
        elif _facilities and area_id and not area_name and not _selected_days:
            try:
                try:
                    parking_area=ParkingArea.objects.get(uid=area_id)
                except ParkingArea.DoesNotExist:
                    return JsonResponse({"message":"area not found!","status":400},status=400)
                
                prev_facilities=[i.facility.uid for i in FacilityChargesForArea.objects.filter(area__uid=area_id)]
                print(prev_facilities)
                incoming_facilities=[i.get('id') for i in _facilities]
                print(incoming_facilities)
                missing_facilities=list(set(prev_facilities)-set(incoming_facilities))

                for facility_id in missing_facilities:
                    existing_facility=FacilityChargesForArea.objects.filter(area__uid=area_id,facility__uid=facility_id)
                    existing_facility_obj=existing_facility[0]
                    existing_facility_obj.is_active=False
                    existing_facility_obj.save()

                for facility in _facilities:
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

                return JsonResponse({"message":"area facilities are updated!","status":200},status=200)
            
            except Exception as e:
                print(e)
                return JsonResponse({"message":"something is wrong!","status":500},status=500)
        
        # update timings
        elif _selected_days and area_id and not area_name and not _facilities:
            try:
                try:
                    parking_area=ParkingArea.objects.get(uid=area_id)
                except ParkingArea.DoesNotExist:
                    return JsonResponse({"message":"area not found!","status":400},status=400)
                
                prev_days=[i.day for i in ParkingAreaOpenCloseTime.objects.filter(area__uid=area_id)]
                incoming_days=[i.get('day') for i in _selected_days]
                missing_days=list(set(prev_days)-set(incoming_days))

                for day in missing_days:
                    existing_timing=ParkingAreaOpenCloseTime.objects.filter(area__uid=area_id,day=day)[0]
                    existing_timing.is_active=False
                    existing_timing.save()

                for timing in _selected_days:
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

                return JsonResponse({"message":"area timings are updated!","status":200},status=200)
            except Exception as e:
                print(e)
                return JsonResponse({"message":"something is wrong!","status":500},status=500)
        else:
            return JsonResponse({"message":"bad request!","status":400},status=400)

@method_decorator(csrf_exempt, name='dispatch')
class GetParkingAreas(View):

    @login_required(login_url="/admins/login",json_response=True)
    def get(self,request):
        try:
            page=request.GET.get('page')
            page_size=request.GET.get('page-size')
            user_id=request._user.get('user_id')
            areas=ParkingArea.objects.filter(admin__uid=user_id).order_by('created_at')
            total_records=areas.count()
            paginator=Paginator(areas,int(page_size))

            try:
                area=paginator.page(int(page))
            except PageNotAnInteger:
                area=paginator.page(1)
            except EmptyPage:
                area=[]
            areas=ParkingAreaSerializer(area,many=True).data
            return JsonResponse({"areas":areas,"total_records":total_records,"status":200},status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"message":"something is wrong!","status":500},status=500)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteParkingArea(View):

    @login_required(login_url="/admins/login",json_response=True)
    def delete(self,request,id):
        try:
            user_id=request._user.get('user_id')
            admin=Admin.objects.get(uid=user_id)
            parking_area=ParkingArea.objects.get(uid=id)
            delete_link=f"{config('BASE_URL')}/admins/delete-confirm-area/{encrypt(user_id)}&{encrypt(parking_area.uid)}"
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
            return JsonResponse({"message":"confirmation link is sent to your email!","status":200},status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"message":"something is wrong!","status":500},status=500)


class ConfirmDeleteParkingArea(View):

    def get(self,request,admin_id,area_id):
        delete_link=f"{config('BASE_URL')}/admins/delete-confirm-area/{admin_id}&{area_id}"
        admin_id=decrypt(admin_id)
        area_id=decrypt(area_id)
        try:
            parking_area=ParkingArea.objects.get(uid=area_id)
        except ParkingArea.DoesNotExist:
            return HttpResponse("Not Found")
        if not EmailVerifyLinkSession.objects.filter(user_id=admin_id,link=delete_link).exists():
            return HttpResponse("Not Found")
        link_session=EmailVerifyLinkSession.objects.filter(user_id=admin_id,link=delete_link)[0]
        if link_session.will_expire_at<timezone.now():
            link_session.delete()
            return HttpResponse("Not Found")
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
            "area_name":parking_area.area_name
        }
        parking_area.is_active=False
        parking_area.save()
        return render(request,'email_templates/parking_area_delete_confirm.html',context=context)

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):

    def get(self,request):
        return render(request,'admins/register.html')
    
    def post(self,request):
        name=StringBuilder(request.POST.get('name')).normalize_spaces().trim_string().build()
        email=StringBuilder(request.POST.get('email')).normalize_spaces().trim_string().build()
        phone=StringBuilder(request.POST.get('phone')).normalize_spaces().trim_string().build()
        password=StringBuilder(request.POST.get('password')).normalize_spaces().trim_string().build()
        pincode=StringBuilder(request.POST.get('pincode')).normalize_spaces().trim_string().build()
        country=StringBuilder(request.POST.get('countrycode')).normalize_spaces().trim_string().build()
        country_code=CountryCode.objects.get(country=country).country_code
        admin_id=generate_unique_id()

        # create subadmin register qr
        subadmin_register_qr_filename=f"{admin_id}_{generate_unique_id()+str(random.randint(1111,9999))}.png"
        subadmin_register_qr_dest=f'parking_system/areavolentier_registerqr/{subadmin_register_qr_filename}'
        subadmin_register_qr_url=f"{config('BASE_URL')}/sub-admin/register/{encrypt(admin_id)}"
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
            args=('Registered Successfully!',f'Hello {name} Your Account has been created as {role.ui_name}.\nYour UserId is {email} and Password is {password}.',email)
        )
        p.start()

        jwt_builder = JwtBuilder()
        payload = {"user_id": admin.uid, "role": admin.role.role_name}
        tokens = jwt_builder.get_token(payload)
        response=redirect('/admins')
        response.set_cookie('access_token', tokens['access_token'], httponly=True, secure=True)
        response.set_cookie('refresh_token', tokens['refresh_token'], httponly=True, secure=True)
        return response

class SearchCountry(View):

    def get(self,request):
        try:
            query = request.GET.get('search', '').upper()
            print(query)
            records=CountryCode.objects.filter(country__icontains=query)
            results=[]
            for rec in records:
                results.append({
                    "country":rec.country,
                    "code":rec.country_code,
                    "iso":rec.iso_code
                })
            print(results)
            return JsonResponse({"results":results,"status":200},status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"message":"failed to load country!","status":500},500)

class ProfileView(View):

    @login_required(login_url="/admins/login")
    def get(self,request):
        user_id=request._user.get('user_id')
        admin=Admin.objects.get(uid=user_id)
        context={
            "name":admin.name,
            "email":admin.email,
            "phone":admin.phone,
            "pincode":admin.pincode,
            "country_code":admin.country_code,
            "subadmin_register_qr":admin.subadmin_register_qr,
            "joined_at":admin.created_at,
            "role":admin.role
        }
        return render(request,'admins/profile.html',context=context)
