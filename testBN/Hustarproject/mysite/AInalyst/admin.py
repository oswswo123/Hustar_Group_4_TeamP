from django.contrib import admin
from .models import Columns
# Register your models here.

class ColumnsAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Columns)