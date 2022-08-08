# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    path('tables.html', views.tables, name='tables'),
    path('tables.html/<int:report_id>', views.tables_detail, name='tables_detail'),
    # re_path(r'^.*\.*', views.pages, name='pages'),
    # path('report/', views.report, name='home'),

]
