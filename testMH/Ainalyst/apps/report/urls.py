"""
     report/urls.py
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='report'),
    # path('<int:report_id>/', views.detail),
]
