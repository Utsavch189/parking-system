import pyotp
import qrcode
from io import BytesIO
from app.models import TwoFactorVerification

class TwoFactorOTP:

    def __init__(self,secret) -> None:
        self.totp = pyotp.TOTP(secret)

    def create(self,username:str)->str:
        try:
            return self.totp.provisioning_uri(name=username, issuer_name='Easy-Parking')
        except Exception as e:
            raise Exception(str(e))
    
    def verify(self,otp:str)->bool:
        try:
            return self.totp.verify(otp)
        except Exception as e:
            raise Exception(str(e))

class GenerateQr:

    @staticmethod
    def generate(username:str,user_id:str):
        try:
            otp=TwoFactorOTP(secret=user_id)
            qr=qrcode.make(otp.create(username=username))
            with BytesIO() as bio:
                qr.save(bio)
                qr_bytes = bio.getvalue()

            file_path=f'media/qr/qr_{user_id}.png'

            with open(file_path,'wb') as q:
                q.write(qr_bytes)

            if not TwoFactorVerification.objects.filter(user_id=user_id).exists():
                TwoFactorVerification.objects.create(
                    user_id=user_id,
                    qr_path=file_path
                )
        except Exception as e:
            raise Exception(str(e))
