from django.contrib import admin
from django.urls import path, include
from apps.index import views as index
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("organizations/", views.organizations),
    path("user/organizations", views._User.organizations),
    path("user/invitations", views._User.invitations),
    path("organization/apps", views._Organization.applications),
    path("organization/users", views._Organization.users),
    path("organization/invite", views._Organization.invite)
]
