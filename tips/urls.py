from django.urls import path
from . import views

urlpatterns = [
    path('', views.tip_list, name='tip_list'),
    path('stats/', views.tip_stats, name='tip_stats'),
    path('add/', views.add_tip, name='add_tip'),
    path('calendar/', views.tip_calendar, name='tip_calendar'),
]
