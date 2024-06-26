from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "",
        include(
            ("conversationalbot.urls", "conversationalbot"),
            namespace="conversationalbot",
        ),
    ),
    path("admin/", admin.site.urls, name="admin"),
    path("api-auth/", include("rest_framework.urls")),
]
