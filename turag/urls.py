from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.catalog, name='catalog'),
    path('catalog/<int:pk>/', views.tour_card, name='tour_card'),
]