from django.views import View
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from app.models import Admin,SlotFacility,CountryCode
from utils.decorators.login_requires import login_required
from django.http import JsonResponse,HttpResponse
from app.models import SlotFacility
from django.core.serializers import serialize
import json
from .service import (login,register,
                    create_parking_area,update_parking_area,
                    get_all_parking_areas,parkingarea_delete_confirmation_mail,
                    parkingarea_actual_delete,get_all_attendants,
                    attendant_delete_confirmation_mail,attendant_actual_delete,
                    attendant_verify_toggle,attendant_suspend_toggle
                    )
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):

    def get(self,request):
        if request._user:
            return redirect('/admins')
        return render(request,'admins/login.html')
    
    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')
        message,status_code=login(email,password)
        if status_code==200:
            # logged in
            response = JsonResponse({"message": "Login successful","status":200},status=200)
            response.set_cookie('access_token', message['access_token'], httponly=True, secure=True)
            response.set_cookie('refresh_token', message['refresh_token'], httponly=True, secure=True)
            return response
        return JsonResponse(message,status=status_code)
        
class HomePageView(View):

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

        message,status_code=create_parking_area(user_id,area_name,facilities,selected_days)
        return JsonResponse(message,status=status_code)
    
    @login_required(login_url="/admins/login",json_response=True)
    def put(self,request):
        data = json.loads(request.body.decode('utf-8'))
        area_id=data.get('area_id',None)
        area_name=data.get('area_name',None)
        facilities=data.get('facilities',None)
        selected_days=data.get('selected_days',None)
        user_id=request._user.get('user_id')

        message,status_code=update_parking_area(user_id,area_id,area_name,facilities,selected_days)
        return JsonResponse(message,status=status_code)

@method_decorator(csrf_exempt, name='dispatch')
class GetParkingAreas(View):

    @login_required(login_url="/admins/login",json_response=True)
    def get(self,request):
        page=request.GET.get('page')
        page_size=request.GET.get('page-size')
        user_id=request._user.get('user_id')
        
        message,status_code=get_all_parking_areas(page,page_size,user_id)
        return JsonResponse(message,status=status_code)

@method_decorator(csrf_exempt, name='dispatch')
class DeleteParkingArea(View):

    @login_required(login_url="/admins/login",json_response=True)
    def delete(self,request,id):
        user_id=request._user.get('user_id')
        message,status_code=parkingarea_delete_confirmation_mail(
            user_id=user_id,
            area_id=id
        )
        return JsonResponse(message,status=status_code)
    
class ConfirmDeleteParkingArea(View):

    def get(self,request,admin_id,area_id):
        stat,context=parkingarea_actual_delete(
            user_id=admin_id, # encrypted id's
            area_id=area_id # encrypted id's
        )
        if not stat:
            return HttpResponse("Not Found")
        return render(request,'email_templates/delete_confirm.html',context=context)

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):

    def get(self,request):
        return render(request,'admins/register.html')
    
    def post(self,request):
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        pincode=request.POST.get('pincode')
        country=request.POST.get('countrycode')
        stat,message,status_code=register(
            name=name,
            email=email,
            phone=phone,
            password=password,
            pincode=pincode,
            country=country
        )
        if stat:
            return redirect('/admins/login')
        return JsonResponse(message,status=status_code)
    
class SearchCountry(View):

    def get(self,request):
        try:
            query = request.GET.get('search', '').upper()
            records=CountryCode.objects.filter(country__icontains=query)
            results=[]
            for rec in records:
                results.append({
                    "country":rec.country,
                    "code":rec.country_code,
                    "iso":rec.iso_code
                })
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

class ParkingAttendantPage(View):

    @login_required(login_url="/admins/login")
    def get(self,request):
        return render(request,'admins/parking_attendant.html')

@method_decorator(csrf_exempt, name='dispatch')
class GetParkingAttendants(View):

    @login_required(login_url="/admins/login",json_response=True)
    def get(self,request):
        page=request.GET.get('page')
        page_size=request.GET.get('page-size')
        user_id=request._user.get('user_id')
        
        message,status_code=get_all_attendants(page,page_size,user_id)
        return JsonResponse(message,status=status_code)
    
@method_decorator(csrf_exempt, name='dispatch')
class DeleteParkingAttendant(View):

    @login_required(login_url="/admins/login",json_response=True)
    def delete(self,request,id):
        user_id=request._user.get('user_id')
        message,status_code=attendant_delete_confirmation_mail(
            user_id=user_id,
            attendant_id=id
        )
        return JsonResponse(message,status=status_code)
            
class ConfirmDeleteParkingAttendant(View):

    def get(self,request,admin_id,attendant_id):
        stat,context=attendant_actual_delete(
            user_id=admin_id, # encrypted id's
            attendant_id=attendant_id # encrypted id's
        )
        if not stat:
            return HttpResponse("Not Found")
        return render(request,'email_templates/delete_confirm.html',context=context)

@method_decorator(csrf_exempt, name='dispatch')
class VerifyParkingAttendant(View):

    @login_required(login_url="/admins/login",json_response=True)
    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        attendant_id=data.get('attendant_id')
        message,status_code=attendant_verify_toggle(attendant_id)
        return JsonResponse(message,status=status_code)

@method_decorator(csrf_exempt, name='dispatch')
class SuspendParkingAttendant(View):

    @login_required(login_url="/admins/login",json_response=True)
    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        attendant_id=data.get('attendant_id')
        message,status_code=attendant_suspend_toggle(attendant_id)
        return JsonResponse(message,status=status_code)