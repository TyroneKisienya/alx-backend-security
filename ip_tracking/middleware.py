from .models import RequestLog
from django.utils import timezone
from .models import RequestLog
from django.core.cache import cache
from ip2geotools.databases.noncommercial import DbIpCity

class IPTrackingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_client_ip(request)

        ip = self.get_client_ip(request)
        path = request.path
        method = request.method

        cache_key = f"geo_{ip}"
        geo_data = cache.get(cache_key)

        if not geo_data:
            try:
                response_data = DbIpCity.get(ip, api_key='free')
                geo_data = {
                    "country": response_data.country,
                    "city": response_data.city
                }
            except Exception:
                geo_data = {"country": None, "city": None}

            cache.set(cache_key, geo_data, 60 * 60 * 24)

        RequestLog.objects.create(
            ip_address = ip,
            timestamp = timezone.now(),
            path = request.path,
            method = method,
            country = geo_data.get('country'),
            city = geo_data.get('city')
        )

        response = self.get_response(request)
        return response
    
    def get_client_ip(self,request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")