from django.contrib import admin
from django.urls import path, include
import turag
from turag import views,urls
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', include('turag.urls')),
    path('admin/', admin.site.urls),
    path('index/', turag.views.index, name='index'),
    path('', include('users.urls')),
]
