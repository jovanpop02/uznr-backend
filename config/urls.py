from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

admin.site.site_header = 'UZNR administracija'
admin.site.site_title = 'UZNR admin'
admin.site.index_title = 'Upravljanje sadržajem'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('content.urls')),
    path('api/health', lambda request: JsonResponse({'status': 'ok'})),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
