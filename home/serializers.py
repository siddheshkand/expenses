from rest_framework import serializers
from home import models


class IncomeAndExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IncomeAndExpense
        fields = [
            'pk',
            'date',
            'amount',
            'tags',
            'mode',
            'type',
        ]
