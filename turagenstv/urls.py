from django.contrib import admin
from django.urls import path
import turag
from turag import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', turag.views.index, name='index'),
    path('catalog/', turag.views.catalog, name='catalog'),
    path('catalog/<int:pk>/', turag.views.tour_detail, name='tour_detail'),
    path('catalog/<int:pk>/review/', turag.views.add_review, name='add_review'),
]
