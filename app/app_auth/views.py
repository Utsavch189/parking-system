from django.views import View
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from utils.otp import OTPSender
from app.models import Admin,SubAdmin,ParkingOwner,Role
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from .service import reset_password

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):

    def post(self,request):
        response=JsonResponse({"message":"Logout successful"},status=200)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

@method_decorator(csrf_exempt, name='dispatch')
class ResetPassword(View):

    def get(self,request):
        if not request._user:
            roles=Role.objects.all()
            return render(request,"forget_password/index.html",context={"roles":roles})
        return HttpResponse("Not Found")

    def post(self,request):
        data = json.loads(request.body.decode('utf-8'))
        email=data.get("email",None)
        new_password=data.get("new_password",None)
        confirm_new_password=data.get("confirm_new_password",None)
        user_type=data.get('user_type',None)
        otp=data.get("otp",None)
        
        message,status_code=reset_password(
            email,
            new_password,
            user_type,
            confirm_new_password,
            otp
        )
        return JsonResponse(message,status=status_code)