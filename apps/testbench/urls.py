from django.contrib import admin
from django.urls import path, include
from apps.testbench import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.landingpage)
]