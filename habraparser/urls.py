from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views

router = DefaultRouter()

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/runner/", views.Runner.as_view()),
    path("admin/", admin.site.urls),

]
