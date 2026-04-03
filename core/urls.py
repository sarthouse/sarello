from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', RedirectView.as_view(url='/contabilidad/', permanent=False), name='home'),
    path('contabilidad/', include('apps.contabilidad.urls')),
    path('tesoreria/', include('apps.tesoreria.urls')),
    path('impuestos/', include('apps.impuestos.urls')),
    path('contactos/', include('apps.contactos.urls')),
    path('configuracion/', include('apps.configuracion.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
