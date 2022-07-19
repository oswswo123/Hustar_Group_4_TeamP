import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Columns(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.BigAutoField
    create_date = models.DateTimeField()
    subject = models.CharField(max_length=200)
    opinion = models.TextField()
    writer = models.CharField(max_length=50)
    stock_firm = models.CharField(max_length=50)
    pdf_file = models.TextField()
    company_inf = models.TextField()
    chart = models.TextField()
    fair_price = models.TextField()

    def __str__(self):
        return self.subject
