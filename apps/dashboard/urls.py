"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views as dashboardViews

urlpatterns = [
    path("", dashboardViews.entry),
    path("organizations/", dashboardViews.organizations),
    path("organization/<int:id>", dashboardViews.summary),
    path("organization/<int:id>/apps", dashboardViews.applications),
    path("organization/<int:id>/users", dashboardViews.users),
    path("organization/<int:id>/licenses", dashboardViews.all_licenses),
    path("organization/<int:id>/licenses/new", dashboardViews.new_license),
    path("organization/<int:id>/app/<int:app_id>", dashboardViews.app),
    path("organization/<int:id>/app/<int:app_id>/license/new", dashboardViews.new_license),
    path("organization/<int:id>/app/<int:app_id>/license/<int:lic_id>", dashboardViews.license)
]
