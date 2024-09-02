import time
from django.http import HttpResponse

class ThrottleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_timestamps = {}

    def __call__(self, request):
        ip = self.get_client_ip(request)
        now = time.time()
        if ip not in self.request_timestamps:
            self.request_timestamps[ip] = []

        self.request_timestamps[ip] = [timestamp for timestamp in self.request_timestamps[ip] if now - timestamp < 60]

        if len(self.request_timestamps[ip]) > 100:  # Limit to 100 requests per minute
            return HttpResponse("Too Many Requests")

        self.request_timestamps[ip].append(now)
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
