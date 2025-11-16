from django.shortcuts import render
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from .models import RequestLog, SuspiciousIP

# ==============================
# Login view (unchanged)
# ==============================
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@ratelimit(key='user_or_ip', rate='10/m', method='POST', block=True)
def login_view(request):
    if request.method == 'POST':
        return JsonResponse({"message": "Login attempt processed"})
    return JsonResponse({"error": "Only POST allowed"}, status=405)


# ==============================
# Track view for /track/
# ==============================
def track_view(request):
    logs = RequestLog.objects.all().order_by('-timestamp')[:10]  # latest 10 logs
    data = [
        {
            "ip": log.ip_address,
            "path": log.path,
            "method": log.method,
            "country": log.country,
            "city": log.city,
            "timestamp": log.timestamp
        }
        for log in logs
    ]
    return JsonResponse(data, safe=False)


# ==============================
# Home page view for /
# ==============================
def home_view(request):
    recent_suspicious = SuspiciousIP.objects.all().order_by('-created_at')[:10]  # latest 10 suspicious IPs
    data = [
        {
            "ip": ip.ip_address,
            "reason": ip.reason,
            "created_at": ip.created_at
        }
        for ip in recent_suspicious
    ]
    return JsonResponse({
        "message": "Welcome to ALX Backend Security",
        "recent_suspicious_ips": data
    })
