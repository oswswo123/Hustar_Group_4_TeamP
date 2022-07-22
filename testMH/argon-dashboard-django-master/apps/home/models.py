# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Report(models.Model):
    report_id = models.CharField(max_length=20, unique=True)
    create_date = models.CharField(max_length=10)   # 작성일
    subject = models.CharField(max_length=200)  # 제목
    price = models.CharField(max_length=20)    # 가격
    opinion = models.CharField(max_length=10, null=True, blank=True)   # 투자 의견
    writer = models.CharField(max_length=20)    # 작성
    stock_firm = models.CharField(max_length=20)    # 증권사

    def __str__(self):
        return self


class Inference(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    new_opinion = models.CharField(max_length=10)   # 새로운 투자 의견