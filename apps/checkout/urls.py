from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("<int:licenseId>", views.checkoutPage),
    path("<str:sessionId>/<int:licenseId>/success", views.checkoutSuccess),
    path("<str:sessionId>/<int:licenseId>/cancelled", views.checkoutCancelled)
]