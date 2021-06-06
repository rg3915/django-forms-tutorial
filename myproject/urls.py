from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('', include('myproject.core.urls', namespace='core')),
    path('accounts/', include('myproject.accounts.urls')),  # without namespace
    path('crm/', include('myproject.crm.urls', namespace='crm')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
