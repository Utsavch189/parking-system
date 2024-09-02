from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from django.conf import settings
import traceback
from app.models import ErrorLog
from utils.id_generator import generate_unique_id

def get_response(exc):
    if isinstance(exc,APIException):
        return Response(data={"message":str(exc)},status=exc.status_code)
    return Response(data={"message":str(exc)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def error_log(exc,context):
    view = context.get('view')
    request = context.get('request')

    user_id=request.token.get('user_id') if hasattr(request,'token') else None
    user_type=request.token.get('role') if hasattr(request,'token') else None
    error_message = str(exc)
    request_method = request.method if request else None
    request_headers = dict(request.headers) if request else None
    request_parameters = dict(request.query_params) if request else None
    request_body = request.data if request else None
    client_ip = request.META.get('REMOTE_ADDR') if request else None
    stack_trace = str(traceback.format_tb(exc.__traceback__)) if hasattr(exc, '__traceback__') else None
    exception_type = type(exc).__name__
    view_name = view.__class__.__name__ if view else None
    response_status_code = exc.get_codes() if isinstance(exc,APIException) else 500
    environment = 'development' if settings.DEBUG else 'production'
    error_location = None
    if view:
        module_name = view.__class__.__module__
        class_name = view.__class__.__name__
        
        if hasattr(view, '__name__'):
            function_name = view.__name__
            error_location = f"{module_name}.{function_name}"
        else:
            error_location = f"{module_name}.{class_name}"

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

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    if exc:
        error_log(exc,context)
        return get_response(exc)

    return response