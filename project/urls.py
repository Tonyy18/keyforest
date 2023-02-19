
from django.contrib import admin
from django.urls import path, include
from apps.index import views as index
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", index.landingpage),
    path("signin", index.signin),
    path("register", index.register),
    path("logout", index.logout),
    path("dashboard/", include("apps.dashboard.urls")),
    path("api/", include("apps.api.urls")),
    path("testbench/", include("apps.testbench.urls")),
    path("market/", include("apps.marketplace.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
