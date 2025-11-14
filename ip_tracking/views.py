from django.shortcuts import render
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit

# Create your views here.

@ratelimit(key = 'ip', rate = '5/m', method = 'POST', block = True)
@ratelimit(key = 'user_or_ip', rate = '10/m', method = 'POST', block = True)

def login_view(request):
    if request.method == 'POST':
        return JsonResponse({"message": "Login attempt processed"})
    return JsonResponse({"error": "Only Post allowed"}, status=405)