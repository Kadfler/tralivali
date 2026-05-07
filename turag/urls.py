from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.catalog, name='catalog'),
    path('catalog/<int:pk>/', tour_detail, name='tour_detail'),
    path('catalog/<int:pk>/review/', add_review, name='add_review'),
]