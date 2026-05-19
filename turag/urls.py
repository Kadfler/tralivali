from django.urls import path
from . import views
from .views import *
import turag
from turag import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.catalog, name='catalog'),
    path('catalog/<int:pk>/', tour_detail, name='tour_detail'),
    path('catalog/<int:pk>/review/', add_review, name='add_review'),
    path('catalog/', turag.views.catalog, name='catalog'),
    path('catalog/<int:pk>/', turag.views.tour_detail, name='tour_detail'),
    path('catalog/<int:pk>/review/', turag.views.add_review, name='add_review'),
    path('profile/', views.profile_view, name='profile'),
    path('tour/<int:tour_id>/book/', views.book_tour_view, name='book_tour'),
]
