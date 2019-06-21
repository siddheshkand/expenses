from django import forms
from . import models


class IncomeExpenseCreationForm(forms.ModelForm):
    tags = forms.CharField()

    class Meta:
        model = models.IncomeAndExpense
        fields = (
            'date',
            'amount',
            'tags',
            'mode',
        )