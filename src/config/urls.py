from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

docs_urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "",
        SpectacularSwaggerView.as_view(
            url_name="api:schema",
        ),
        name="docs",
    ),
]

v1_urlpatterns = [
    path("topics/", include("src.apps.topics.urls", namespace="topics")),
]

api_urlpatterns = [
    path("docs/", include(docs_urlpatterns)),
    path("v1/", include((v1_urlpatterns, "v1"), namespace="v1")),
]

urlpatterns = [
    path("waltz/admin/", admin.site.urls),
    path(
        "waltz/api/",
        include((api_urlpatterns, "api"), namespace="api"),
    ),
]
