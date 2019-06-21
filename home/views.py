from django.db.models import Sum, Q
from django.forms import formset_factory
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from . import forms, models


def home(request):
    form = forms.IncomeExpenseCreationForm
    form_set_expenses = formset_factory(forms.IncomeExpenseCreationForm, extra=4)
    form_set_income = formset_factory(forms.IncomeExpenseCreationForm, extra=4)
    incomeAndExpense = models.IncomeAndExpense.objects.all()

    # For Bank
    bank_income_total = models.IncomeAndExpense.objects.filter(type='income').filter(
        ~Q(mode__contains='cash')).aggregate(
        Sum('amount')).get(
        'amount__sum') or 0
    bank_expense_total = models.IncomeAndExpense.objects.filter(type='expense').filter(
        ~Q(mode__contains='cash')).aggregate(
        Sum('amount')).get(
        'amount__sum') or 0
    # For In hand Cash
    cash_income_total = models.IncomeAndExpense.objects.filter(type='income').filter(
        Q(mode__contains='cash')).aggregate(
        Sum('amount')).get(
        'amount__sum') or 0
    cash_expense_total = models.IncomeAndExpense.objects.filter(type='expense').filter(
        Q(mode__contains='cash')).aggregate(
        Sum('amount')).get(
        'amount__sum') or 0

    bank_balance = bank_income_total - bank_expense_total
    cash_balance = cash_income_total - cash_expense_total
    total = bank_balance + cash_balance
    context = {
        'form': form,
        'incomeAndExpense': incomeAndExpense,
        'form_set_expenses': form_set_expenses,
        'form_set_income': form_set_income,
        'bank_balance': bank_balance,
        'cash_balance': cash_balance,
        'total': total,
    }
    return render(request, 'home/home.html', context)


def expenses_create_formset(request):
    if request.method == 'POST':
        IncomeExpensesCreationFormSet = formset_factory(forms.IncomeExpenseCreationForm)
        form_set = IncomeExpensesCreationFormSet(request.POST or None)
        if form_set.is_valid():
            for form in form_set:
                if form.cleaned_data != {}:
                    temp = form.save(commit=False)
                    temp.type = 'expense'
                    temp.save()
        return redirect('/')


def income_create_formset(request):
    if request.method == 'POST':
        IncomeExpensesCreationFormSet = formset_factory(forms.IncomeExpenseCreationForm)
        form_set = IncomeExpensesCreationFormSet(request.POST or None)
        if form_set.is_valid():
            for form in form_set:
                if form.cleaned_data != {}:
                    temp = form.save(commit=False)
                    temp.type = 'income'
                    temp.save()
        return redirect('/')
