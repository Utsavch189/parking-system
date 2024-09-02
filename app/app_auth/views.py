from django.views import View
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from utils.otp import OTPSender
from app.models import Admin,SubAdmin,ParkingOwner,Role
from django.contrib.auth.hashers import make_password

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
        roles=Role.objects.all()
        return render(request,"forget_password/index.html",context={"roles":roles})

    def post(self,request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            email=data.get("email",None)
            new_password=data.get("new_password",None)
            confirm_new_password=data.get("confirm_new_password",None)
            user_type=data.get('user_type',None)
            otp=data.get("otp",None)
            
            if otp and email and new_password and user_type:
            
                status,message=OTPSender.verify(
                    email,
                    int(otp)
                )

                if not status:
                    return JsonResponse({"message":message,"status":400},status=400)
                
                if user_type.upper()=='ADMIN':
                    try:
                        user=Admin.objects.get(email=email)
                    except Admin.DoesNotExist:
                        return JsonResponse({"message":"user doesn't exists!","status":400},status=400)
                
                elif user_type.upper()=='SUBADMIN':
                    try:
                        user=SubAdmin.objects.get(email=email)
                    except SubAdmin.DoesNotExist:
                        return JsonResponse({"message":"user doesn't exists!","status":400},status=400)
                
                elif user_type.upper()=='PARKINGOWNER':
                    try:
                        user=ParkingOwner.objects.get(email=email)
                    except ParkingOwner.DoesNotExist:
                        return JsonResponse({"message":"user doesn't exists!","status":400},status=400)
                
                else:
                    return JsonResponse({"message":"invalid user role!","status":400},status=400)
                
                user.password=make_password(new_password)
                user.save()
                
                return JsonResponse({"message":"password is changed!","status":200},status=200)

            elif email and new_password and confirm_new_password and user_type:
                if user_type.upper()=='ADMIN':
                    try:
                        user=Admin.objects.get(email=email)
                    except Admin.DoesNotExist:
                        return JsonResponse({"message":"user doesn't exists!","status":400},status=400)
                
                elif user_type.upper()=='SUBADMIN':
                    try:
                        user=SubAdmin.objects.get(email=email)
                    except SubAdmin.DoesNotExist:
                        return JsonResponse({"message":"user doesn't exists!","status":400},status=400)
                
                elif user_type.upper()=='PARKINGOWNER':
                    try:
                        user=ParkingOwner.objects.get(email=email)
                    except ParkingOwner.DoesNotExist:
                        return JsonResponse({"message":"user doesn't exists!","status":400},status=400)
                
                else:
                    return JsonResponse({"message":"invalid user role!","status":400},status=400)
                
                if not new_password==confirm_new_password:
                    return JsonResponse({"message":"passwords are not matching!","status":400},status=400)
                
                OTPSender.send(
                    to=email,
                    user_id=email,
                    name=user.name
                )
                return JsonResponse({"message":"otp sent to your email!","status":200},status=200)
            
            return JsonResponse({"message":"bad request!","status":400},status=400)
        
        except Exception as e:
            return JsonResponse({"message":str(e),"status":500},status=500)