from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from anki.views import HomeView
from kaos.sites import custom_admin_site

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", custom_admin_site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
