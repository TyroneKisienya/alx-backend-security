from django.urls import path
from .views import login_view

urlpattern = [
    path('login/', login_view, name='rate_limited_login'),
]