from typing import Tuple
from utils.otp import OTPSender
from django.contrib.auth.hashers import make_password
from app.models import Admin,SubAdmin,ParkingOwner,Role

def reset_password(email:str,new_password:str,user_type:str,confirm_new_password:str="",otp:str="")->Tuple[dict,int]:
    try:

        if user_type.upper()=='ADMIN':
                try:
                    user=Admin.objects.get(email=email)
                except Admin.DoesNotExist:
                    return {"message":"user doesn't exists!","status":400},400
            
        elif user_type.upper()=='SUBADMIN':
            try:
                user=SubAdmin.objects.get(email=email)
            except SubAdmin.DoesNotExist:
                return {"message":"user doesn't exists!","status":400},400
        
        elif user_type.upper()=='PARKINGOWNER':
            try:
                user=ParkingOwner.objects.get(email=email)
            except ParkingOwner.DoesNotExist:
                return {"message":"user doesn't exists!","status":400},400
        
        else:
            return {"message":"invalid user role!","status":400},400

        if otp and email and new_password and user_type:
            
            status,message=OTPSender.verify(
                email,
                int(otp)
            )
            if not status:
                return {"message":message,"status":400},400
            
            user.password=make_password(new_password)
            user.save()
            
            return {"message":"password is changed!","status":200},200

        elif email and new_password and confirm_new_password and user_type:

            if not new_password==confirm_new_password:
                return {"message":"passwords are not matching!","status":400},400
            
            OTPSender.send(
                to=email,
                user_id=email,
                name=user.name
            )
            return {"message":"otp sent to your email!","status":200},200
        
        return {"message":"bad request!","status":400},400
    except Exception as e:
        return {"message":"something is wrong!","status":500},500