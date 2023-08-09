from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("doc/", SpectacularAPIView.as_view(), name="schema"),
    path("doc/redoc", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", include("djoser.urls")),
    path("", include("apps.log.urls")),
    path("", include("apps.country.urls")),
    path("", include("apps.region.urls")),
    path("", include("apps.category.urls")),
    path("", include("apps.area.urls")),
    path("", include("apps.role.urls")),
    path("", include("apps.user.urls")),
    path("", include("apps.type_process.urls")),
    path("", include("apps.type_process_mail.urls")),
    path("", include("apps.status_process.urls")),
    path("", include("apps.status_process_tran.urls")),
    path("", include("apps.status_process_mail.urls")),
    path("", include("apps.process.urls")),
    path("", include("apps.process_tran.urls")),
    path("", include("apps.process_mov.urls")),
    path("", include("apps.process_act.urls")),
    path("", include("apps.process_mail.urls")),
]
