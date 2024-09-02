from utils.jwt_builder import JwtBuilder 
import json

class JwtAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        access_token = request.COOKIES.get('access_token',None)
        refresh_token = request.COOKIES.get('refresh_token',None)
        jwt_builder = JwtBuilder()
        setattr(request,'need_refresh',False)
        setattr(request,'logout',False)
        setattr(request,'_user',None)

        if access_token:
            payload = jwt_builder.decode(access_token)
            if payload:
                request._user = json.dumps({
                    "user_id":payload.get("user_id"),
                    "role":payload.get("role")
                })
            else:
                if refresh_token:
                    payload = jwt_builder.decode(refresh_token)
                    if payload:
                        request._user = json.dumps({
                            "user_id":payload.get("user_id"),
                            "role":payload.get("role")
                        })
                        setattr(request,'need_refresh',True)
                    else:
                        setattr(request,'logout',True)

        response = self.get_response(request)
        print("request.need_refresh : ",request.need_refresh)
        print("request.logout : ",request.logout)
        # Process response
        if request.need_refresh:
            print('refreshed...')
            if type(request._user)==str:
                new_tokens = jwt_builder.get_token(payload=json.loads(request._user))
            elif type(request._user)==dict:
                new_tokens = jwt_builder.get_token(payload=request._user)
                
            response.set_cookie('access_token', new_tokens['access_token'], httponly=True, secure=True)
            response.set_cookie('refresh_token', new_tokens['refresh_token'], httponly=True, secure=True)
            return response

        if request.logout:
            print('logout...')
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response
        
        return response
