from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/library/', include('src.library_backend.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
