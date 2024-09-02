import random
from app.models import OTP
from utils.emails import SendMail
from datetime import datetime,timedelta
from multiprocessing import Process
from django.utils import timezone

class OTPSender:

    @staticmethod
    def send(to:str,user_id:str,name:str=""):
        try:
            otp=random.randint(111111,999999)
            if name:
                body=f"Hello {name} your OTP is {otp} and valid for next 3 minutes."
            else:
                body=f"Your OTP is {otp} and valid for next 3 minutes."
            
            p=Process(
                target=SendMail.send_email,
                args=(
                    "OTP Verification",
                    body,
                    to
                )
            )
            p.start()
            if OTP.objects.filter(user_id=user_id).exists():
                otp_obj=OTP.objects.get(user_id=user_id)
                otp_obj.otp=otp
                otp_obj.created_at=datetime.now()
                otp_obj.will_expire_at=datetime.now()+timedelta(minutes=3)
                otp_obj.save()
            else:
                OTP.objects.create(
                    user_id=user_id,
                    otp=otp,
                    created_at=datetime.now(),
                    will_expire_at=datetime.now()+timedelta(minutes=3)
                )
        except Exception as e:
            raise Exception(str(e))
    
    @staticmethod
    def verify(user_id:str,_otp:int)->tuple:
        try:
            if not OTP.objects.filter(user_id=user_id).exists():
                return False,"OTP doesn't exists!"
            
            otp=OTP.objects.get(user_id=user_id)

            if otp.will_expire_at<timezone.now() or int(otp.otp)!=int(_otp):
                return False,"OTP is invalid!"
            
            otp.delete()
            return True,"Verified"
        except Exception as e:
            raise Exception(str(e))

