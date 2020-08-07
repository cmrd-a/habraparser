from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views

router = DefaultRouter()
router.register("articles", views.ArticleViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/force_parsing/", views.ForceParsing.as_view()),
    path("admin/", admin.site.urls),
]
