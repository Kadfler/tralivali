from django.contrib import admin
from django.urls import path, include
import turag
from turag import views,urls
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('turag.urls')),
    path('admin/', admin.site.urls),
    path('index/', turag.views.index, name='index'),
    path('', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)