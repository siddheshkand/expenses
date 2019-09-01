from django.contrib import admin
from . import models


class MyAdminIncome(admin.ModelAdmin):
    list_display = [
        'id',
        'date',
        'amount',
        'tags',
        'mode',
        'type',
    ]


class MyAdminSchedule(admin.ModelAdmin):
    list_display = [
        'event_name',
        'date',
        'from_time',
        'to_time',
        'location',
    ]


admin.site.register(models.IncomeAndExpense, MyAdminIncome)
admin.site.register(models.Scheduler, MyAdminSchedule)
