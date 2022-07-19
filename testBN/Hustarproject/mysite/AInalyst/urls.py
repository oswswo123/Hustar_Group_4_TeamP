from django.urls import path

from . import views

app_name = 'AInalyst'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:columns_id>/', views.detail, name='detail'),

]