from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.jwt_builder import JwtBuilder
from utils.id_generator import generate_unique_id
from utils import exceptions
from django.contrib.auth.hashers import make_password
from utils.decorators.authorize import is_authorize
from utils.otp import OTPSender
from utils.two_factor_auth import TwoFactorOTP,GenerateQr

class RegisterView(APIView):

    def post(self,request):
        tokens={}
        return Response({"message":"registered!","token":tokens if tokens else {}},status=status.HTTP_201_CREATED)

class LoginView(APIView):

    def post(self,request):
        data=request.data
        username=data.get('username') # might be email or mobile
        password=data.get('password')

        jwt_payload={
        }

        tokens=JwtBuilder(payload=jwt_payload).get_token()
        
        return Response({"message":"login!","token":tokens if tokens else {}},status=status.HTTP_200_OK)


class RefreshTokenView(APIView):

    @is_authorize()
    def get(self,request):
        token_data=request.token_data
            
        jwt_payload={
        }
        tokens=JwtBuilder(payload=jwt_payload).get_token()
        
        return Response({"message":"new tokens!","token":tokens},status=status.HTTP_201_CREATED)


class ForgetPasswordView(APIView):

    def post(self,request):
        data=request.data
        username=data.get('username') # might be email or mobile
        new_password=data.get('new_password')
        
        return Response({"message":"password is updated!"},status=status.HTTP_200_OK)


class OTPSendView(APIView):

    def post(self,request):
        data=request.data
        email=data.get("email",None)
        user_id=None
        name=None

        OTPSender.send(
            to=email,
            user_id=user_id,
            name=name
        )

        return Response({"message":"OTP send!"},status=status.HTTP_201_CREATED)

        
class OTPVerifyView(APIView):

    def post(self,request):
        data=request.data
        email=data.get("email",None)
        otp=data.get("otp",None)
        user_id=None
        sts,message=OTPSender.verify(
            user_id,
            otp
        )
        if not sts:
            return Response({"message":message,"verified":False},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message":message,"verified":True},status=status.HTTP_200_OK)


class TwoFactorCreateView(APIView):

    def post(self,request):
        data=request.data
        user_id=data.get('user_id',None)
        name=None
        GenerateQr.generate(
            username=name,
            user_id=user_id
        )
        return Response({"message":"qr generated"},status=status.HTTP_201_CREATED)



class TwoFactorVerifyView(APIView):

    def post(self,request):
        data=request.data
        user_id=data.get('user_id',None)
        otp=data.get('otp',None)

        otp_obj=TwoFactorOTP(user_id)

        if not otp_obj.verify(
            otp=otp
        ):
            return Response({"message":"wrong otp!","verified":False},status=status.HTTP_200_OK)
        
            
        return Response({"message":"verified!","verified":True},status=status.HTTP_200_OK)
