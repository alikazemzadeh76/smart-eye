from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import set_language
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from django.conf import settings


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("i18n/", set_language, name='set_language'),
    path('admin/', admin.site.urls),
    path('', include('account_app.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)