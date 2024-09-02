from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from django.conf import settings
import traceback
from app.models import ErrorLog
from utils.id_generator import generate_unique_id
import json

class BufferRequestBodyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            if request.method in ['POST', 'PUT', 'PATCH','DELETE']:
                request.buffered_body = request.body
            else:
                request.buffered_body = None
        except:
            request.buffered_body = None

class GlobalExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        # Log the exception
        self.log_error(request, exception)

        # Return a custom error response
        response = render(request,'server_error.html')
        return response
    
    
    def log_error(self, request, exception):

        try:
            if request.buffered_body:
                body=request.buffered_body.decode('utf-8')
            else:
                body=None
        except:
            body=None

        print(type(request._user))
        if request._user :
            if type(request._user)==str:
                request.user=json.loads(request._user)
        else:
            request._user=None


        user_id = request._user.get('user_id') if request._user else ""
        user_type = request._user.get('role') if request._user else ""
        error_message = str(exception)
        request_method = request.method
        request_headers = dict(request.headers)
        request_parameters = dict(request.GET)
        request_body = body
        client_ip = request.META.get('REMOTE_ADDR')
        stack_trace = str(traceback.format_exc())
        exception_type = type(exception).__name__
        view_name = getattr(request.resolver_match.func, '__name__', None) if request.resolver_match else None
        response_status_code = 500
        environment = 'development' if settings.DEBUG else 'production'
        error_location = None  # Needs specific context to be set accurately

        # Create ErrorLog entry
        ErrorLog.objects.create(
            uid=generate_unique_id(),
            error_message=error_message,
            user_id=user_id,
            user_type=user_type,
            request_method=request_method,
            request_headers=request_headers,
            request_parameters=request_parameters,
            request_body=request_body,
            client_ip=client_ip,
            stack_trace=stack_trace,
            exception_type=exception_type,
            view_name=view_name,
            response_status_code=response_status_code,
            enviroment=environment,
            error_location=error_location
        )