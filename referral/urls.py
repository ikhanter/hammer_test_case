"""
URL configuration for hammer_test_case project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include



from referral.views import IndexUsersAPIView, ConfirmCodeAPIView, DetailAPIView, LogoutView


urlpatterns = [
    path('', IndexUsersAPIView.as_view(), name='index'),
    path('me/', DetailAPIView.as_view(), name='me'),
    path('confirm/', ConfirmCodeAPIView.as_view(), name='confirm_endpoint'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
