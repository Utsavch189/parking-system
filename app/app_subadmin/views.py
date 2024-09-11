from django.views import View
from django.shortcuts import render,redirect
from django.http import JsonResponse,Http404,HttpResponse
from utils.decorators.login_requires import login_required
from utils.string import StringBuilder
from utils.encrypt import encrypt,decrypt
from django.db import transaction
from utils.id_generator import generate_unique_id
from datetime import datetime,timedelta
from utils.emails import SendMail
from decouple import config
from multiprocessing import Process
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from app.models import Admin,SubAdmin,ParkingArea,Role,SubAdminUnderParkingArea
import json
from .service import login,register

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):

    def get(self,request):
        if request._user:
            return redirect('/sub-admin')
        return render(request,'subadmin/login.html')

    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')
        response=login(email,password)
        return response
        
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):

    def get(self,request,admin_id):
        enc_id=admin_id
        try:
            admin_id=decrypt(enc_id)
        except Exception as e:
            return HttpResponse("Not Found")
        admin=Admin.objects.get(uid=admin_id)
        areas=ParkingArea.objects.filter(admin__uid=admin_id)
        return render(request,'subadmin/register.html',context={"admin":admin,"areas":areas,"enc_id":enc_id})
    
    def post(self,request,admin_id):
        enc_id=admin_id
        try:
            admin_id=decrypt(enc_id)
        except Exception as e:
            return HttpResponse("Not Found")
        name=StringBuilder(request.POST.get('name')).normalize_spaces().trim_string().build()
        email=StringBuilder(request.POST.get('email')).normalize_spaces().trim_string().build()
        phone=StringBuilder(request.POST.get('phone')).normalize_spaces().trim_string().build()
        password=StringBuilder(request.POST.get('password')).normalize_spaces().trim_string().build()
        parking_areas=StringBuilder(request.POST.get('parking_areas')).normalize_spaces().trim_string().build()
        role=Role.objects.get(role_name='SUBADMIN')
        response=register(
            admin_id,name,email,phone,password,parking_areas.split(","),role
        )
        return response

class Home(View):

    @login_required(login_url="/sub-admin/login")
    def get(self,request):
        return render(request,'subadmin/home.html')