from django.utils import timezone
from app.models import AccessLog
from decouple import config
from utils.id_generator import generate_unique_id
from django.utils.deprecation import MiddlewareMixin

class BufferRequestBodyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            if request.method in ['POST', 'PUT', 'PATCH','DELETE']:
                request.buffered_body = request.body
            else:
                request.buffered_body = None
        except:
            request.buffered_body = None


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        start_time = timezone.now()

        response = self.get_response(request)

        # Process response
        end_time = timezone.now()
        duration = end_time - start_time
        if response.status_code>=400:
            pass
        else:
            self.log_access(request, response, start_time, duration)

        return response

    def log_access(self, request, response, start_time, duration):
        # Extract relevant information from the request and response
        
        try:
            if request.buffered_body:
                body=request.buffered_body.decode('utf-8')
            else:
                body=None
        except:
            body=None

        access_log = AccessLog(
            uid=generate_unique_id(),
            request_method=request.method,
            request_headers=dict(request.headers),
            request_parameters=dict(request.GET),
            request_body= body,
            client_ip=request.META.get('REMOTE_ADDR'),
            view_name=request.resolver_match.view_name if request.resolver_match else None,
            response_status_code=response.status_code,
            environment=config('ENV'),
            created_at=start_time,
            response_content=response.content.decode('utf-8'),
            request_url=request.build_absolute_uri(),
            user_agent=request.headers.get('User-Agent'),
            duration=duration,
            referer=request.headers.get('Referer'),
            request_query_params=dict(request.GET),
            response_headers=dict(response.headers),
        )

        access_log.save()
    