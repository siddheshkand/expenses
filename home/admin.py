from django.contrib import admin
from . import models


class MyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'date',
        'amount',
        'tags',
        'mode',
        'type',
    ]


admin.site.register(models.IncomeAndExpense, MyAdmin)
