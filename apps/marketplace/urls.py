from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.market_index),
    path("q/<str:search_str>", views.search),
]