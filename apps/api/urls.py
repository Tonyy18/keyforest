from django.contrib import admin
from django.urls import path, include
from apps.index import views as index
from django.conf.urls.static import static
from django.conf import settings
from .endpoints import User, Organization, Application, Stripe, License

from . import views

urlpatterns = [
    path("organizations/", views.organizations),
    path("applications/", views.applications),
    path("permissions/", views.permissions),
    path("user/organizations", User.organizations),
    path("user/purchases/<int:id>", User.purchases),
    path("organization/apps", Organization.applications),
    path("organization/users/<int:userid>", Organization.users), #For delete
    path("organization/users", Organization.users), #For get and post
    path("organization/users/<int:userid>/permissions", Organization.permissions),
    path("organization/apps/<int:appid>/licenses", Application.licenses),
    path("organization/apps/<int:appid>/licenses/<int:licenseid>/statistics", License.statistics),
    path("organization/licenses", Organization.licenses),
    path("organization/apps/<int:appid>/statistics", Application.statistics),
    path("organization/stripe/connect/url", Stripe.get_connect_url),
    path("organization/stripe/connect/accounts", Stripe.get_all_connected_accounts),
    path("stripe/checkout/newsession/<int:licenseId>", Stripe.new_session),
    path("stripe/webhook", Stripe.webhook)
]
