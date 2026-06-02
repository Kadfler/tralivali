from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('catalog/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('catalog/<int:pk>/review/', views.add_review, name='add_review'),
    path('profile/', views.profile_view, name='profile'),
    path('tour/<int:tour_id>/book/', views.book_tour, name='book_tour'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('cancel-booking/', views.cancel_booking, name='cancel_booking'),
]
