from django.contrib import admin
from django.urls import path, include
from apps.index import views as index
from django.conf.urls.static import static
from django.conf import settings
from .endpoints import User, Organization, Application

from . import views

urlpatterns = [
    path("organizations/", views.organizations),
    path("user/organizations", User.organizations),
    path("organization/apps", Organization.applications),
    path("organization/users", Organization.users),
    path("organization/permissions", Organization.permissions),
    path("organization/app/license", Application.license),
    path("permissions/", views.permissions),
]
