from django.shortcuts import redirect
import json
from django.http import JsonResponse

def login_required(login_url,json_response=False):
    def _inner(func):
        def _wrapped_view(*args, **kwargs):
            access_token = args[1].COOKIES.get('access_token')
            refresh_token = args[1].COOKIES.get('refresh_token')
            if (not (access_token and refresh_token)) or args[1].logout:
                if not json_response:
                    response=redirect(login_url)
                    response.delete_cookie('access_token')
                    response.delete_cookie('refresh_token')
                    return response
                else:
                    response=JsonResponse({"message":"unauthorized!","status":401,"login_url":login_url},status=401)
                    response.delete_cookie('access_token')
                    response.delete_cookie('refresh_token')
                    return response 
            args[1]._user=json.loads(args[1]._user)
            return func(*args, **kwargs)
        return _wrapped_view
    return _inner
