from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('pages/',include('pages.urls')),
    path('',include('accounts.urls')),
    path('report/',include('report.urls')),
    path('summernote/',include('django_summernote.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)