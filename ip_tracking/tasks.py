from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATH = ['/admin', '/login']

@shared_task
def detect_suspicious_ip():
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)

    logs = RequestLog.objects.filter(timestamp__gte = one_hour_ago)

    ip_count = {}
    for log in logs:
        ip_count[log.ip_address] = ip_count.get(log.ip_address, 0) + 1

        if any(log.path.startswith(p) for p in SENSITIVE_PATH):
            SuspiciousIP.objects.get_or_create(
                ip_address = log.ip_address,
                defaults={"reason": f"Accessed sensitive path: {log.path}"}
            )
    
    for ip, total in ip_count.items():
        if total > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address = ip,
                defaults={"reason": f"Exceeded 100 requests/hour - total: {total}"}
            )
            