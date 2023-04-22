from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.market_index),
    path("search/<str:query>", views.searchPage),
    path("seller/<int:orgId>", views.sellerPage),
    path("seller/<int:orgId>/app/<int:appId>", views.appPage),
    path("buy/<int:licenseId>", views.buyPage)
]