from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # === For Debug Tool Bar ===
    path("__debug__/", include("debug_toolbar.urls"))
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MYFILES_URL, document_root=settings.MYFILES_ROOT)