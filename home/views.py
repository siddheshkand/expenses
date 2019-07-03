import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.forms import formset_factory
from django.shortcuts import redirect, render
# from django.views.generic import CreateView

from . import forms, models
import statistics


def get_stat():
    stats = {}
    if models.IncomeAndExpense.objects.exists():
        start_date = models.IncomeAndExpense.objects.earliest('date').date
        end_date = models.IncomeAndExpense.objects.latest('date').date
        # Iterate over start end
        day = datetime.timedelta(days=1)
        daily_expenses_array = []
        while start_date <= end_date:
            daily_sum = models.IncomeAndExpense.objects.filter(type='expense').filter(date=start_date).aggregate(
                Sum('amount'))['amount__sum']
            if not daily_sum:
                daily_sum = 0
            daily_expenses_array.append(daily_sum)
            start_date = start_date + day
        daily_expenses_median = statistics.median(daily_expenses_array)
        daily_expenses_mean = statistics.mean(daily_expenses_array)
        daily_expenses_mode = statistics.mode(daily_expenses_array)
        # print(daily_expenses_array)
        stats.update({'daily_expenses_mean': int(daily_expenses_mean)})
        stats.update({'daily_expenses_median': int(daily_expenses_median)})
        stats.update({'daily_expenses_mode': int(daily_expenses_mode)})

        return stats


@login_required(login_url='/admin/login/')
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

    stats = get_stat()

    context = {
        'form': form,
        'incomeAndExpense': incomeAndExpense,
        'form_set_expenses': form_set_expenses,
        'form_set_income': form_set_income,
        'bank_balance': bank_balance,
        'cash_balance': cash_balance,
        'total': total,
        'stats': stats
    }
    return render(request, 'home/home.html', context)


@login_required(login_url='/admin/login/')
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


@login_required(login_url='/admin/login/')
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
