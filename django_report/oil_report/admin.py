from django.contrib import admin
from .models import *


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'calc_time', 'date_start', 'date_fin', 'lag', 'status')


@admin.register(DataFrame)
class DataFrameAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'date', 'liquid', 'oil', 'water', 'wct')
