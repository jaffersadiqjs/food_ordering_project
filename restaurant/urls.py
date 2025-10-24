from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('add_item/', views.add_item, name='add_item'),
]
