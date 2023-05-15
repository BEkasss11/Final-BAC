# from django.contrib import admin
# from django.urls import path, include
#
# from django.conf import settings
#
# from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', include('admin.urls')),
    path('', include('main.urls')),
    path('auth/', include('account.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)