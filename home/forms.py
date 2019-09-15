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


class SchedulerForm(forms.ModelForm):
    event_name = forms.CharField()
    location = forms.CharField()
    from_time = forms.TimeInput()
    to_time = forms.TimeInput()

    class Meta:
        model = models.Scheduler
        fields = (
            'event_name',
            'date',
            'from_time',
            'to_time',
            'location',
        )


class PeriodicExpensesForm(forms.ModelForm):
    name = forms.CharField()
    amount = forms.CharField()
    # type = forms.CharField()
    description = forms.CharField()

    class Meta:
        model = models.PeriodicExpense
        fields = [
            "name",
            "amount",
            "type",
            "description",
        ]
