# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Report(models.Model):
    create_date = models.DateField(auto_now_add=True, blank=True)   # 작성일
    company = models.CharField(max_length=50)  # 기업명
    subject = models.CharField(max_length=200)  # 제목
    article = models.TextField(blank=True, null=True)  # 요약문
    opinion = models.CharField(max_length=20, null=True, blank=True)   # 투자 의견
    new_opinion = models.CharField(max_length=20, null=True, blank=True)   # 새로운 투자 의견
    stock_firm = models.CharField(max_length=20)    # 증권사
    filename = models.CharField(max_length=100, null=True, blank=True)  # 파일명
    # price = models.CharField(max_length=20)    # 가격
    # writer = models.CharField(max_length=20)    # 작성


# class Inference(models.Model):
#     report = models.ForeignKey(Report, on_delete=models.CASCADE)
