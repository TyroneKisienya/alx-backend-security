from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('track/', views.track_view, name='track'),
    path('login/', views.login_view, name='login'),
]
