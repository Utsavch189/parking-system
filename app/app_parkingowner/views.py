from django.views import View
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from utils.decorators.login_requires import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .service import login,register
from utils.encrypt import decrypt
from app.models import Admin,ParkingArea,Role
from utils.string import StringBuilder

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):

    def get(self,request):
        if request._user:
            return redirect('/parking-owner')
        return render(request,'parkingowner/login.html')
    
    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')
        message,status_code=login(email,password)
        if status_code==200:
            response = JsonResponse({"message": "Login successful","status":200},status=200)
            response.set_cookie('access_token', message['access_token'], httponly=True, secure=True)
            response.set_cookie('refresh_token', message['refresh_token'], httponly=True, secure=True)
            return response
        return JsonResponse(message,status=status_code)

@method_decorator(csrf_exempt, name='dispatch')
class Register(View):

    def get(self,request,parking_area_id,admin_id):
        enc_parking_area_id=parking_area_id
        enc_admin_id=admin_id
        try:
          parking_area_id=decrypt(parking_area_id)
          admin_id=decrypt(admin_id)
        except Exception as e:
            return HttpResponse("Not Found")
        admin=Admin.objects.get(uid=admin_id)
        parking_area=ParkingArea.objects.get(uid=parking_area_id)
        return render(request,'parkingowner/register.html',context={"admin":admin,"area":parking_area,"enc_parking_area_id":enc_parking_area_id,"enc_admin_id":enc_admin_id})


    def post(self,request,parking_area_id,admin_id):
        try:
          parking_area_id=decrypt(parking_area_id)
          admin_id=decrypt(admin_id)
        except Exception as e:
            return HttpResponse("Not Found")
        name=StringBuilder(request.POST.get('name')).normalize_spaces().trim_string().build()
        email=StringBuilder(request.POST.get('email')).normalize_spaces().trim_string().build()
        phone=StringBuilder(request.POST.get('phone')).normalize_spaces().trim_string().build()
        password=StringBuilder(request.POST.get('password')).normalize_spaces().trim_string().build()
        stat,message,status_code=register(
            admin_id,name,email,phone,password
        )
        if stat:
            return redirect("/parking-owner/login")
        return JsonResponse(message,status=status_code)