import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

admin.site.site_header = 'UZNR administracija'
admin.site.site_title = 'UZNR admin'
admin.site.index_title = 'Upravljanje sadržajem'


def debug_media(request):
    root = str(settings.MEDIA_ROOT)
    exists = os.path.isdir(root)
    news_dir = os.path.join(root, 'news')
    news_files = os.listdir(news_dir)[:10] if os.path.isdir(news_dir) else None
    target = os.path.join(news_dir, '1-za-sajt-876x600.jpg')
    return JsonResponse({
        'MEDIA_ROOT': root,
        'media_root_exists': exists,
        'news_dir_exists': os.path.isdir(news_dir),
        'news_dir_sample': news_files,
        'target_exists': os.path.isfile(target),
        'target_size': os.path.getsize(target) if os.path.isfile(target) else None,
        'cwd': os.getcwd(),
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('content.urls')),
    path('api/health', lambda request: JsonResponse({'status': 'ok'})),
    path('debug/media', debug_media),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
