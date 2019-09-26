import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render
import json
# from django.views.generic import CreateView
from django.core import serializers

from . import forms, models
import statistics
from dateutil.parser import parse


# Utility Function
def get_stat():
    stats = {}
    if models.IncomeAndExpense.objects.exists():
        dates_array = []
        start_date = models.IncomeAndExpense.objects.earliest('date').date
        end_date = models.IncomeAndExpense.objects.latest('date').date
        # Iterate over start end
        day = datetime.timedelta(days=1)
        daily_expenses_array = []
        daily_income_array = []
        while start_date <= end_date:
            daily_sum_expenses = \
                models.IncomeAndExpense.objects.filter(type='expense').filter(date=start_date).aggregate(
                    Sum('amount'))['amount__sum']

            daily_sum_income = \
                models.IncomeAndExpense.objects.filter(type='income').filter(date=start_date).aggregate(
                    Sum('amount'))['amount__sum']
            if not daily_sum_expenses:
                daily_sum_expenses = 0
            if not daily_sum_income:
                daily_sum_income = 0
            daily_expenses_array.append(daily_sum_expenses)
            daily_income_array.append(daily_sum_income)
            dates_array.append(start_date)
            start_date = start_date + day
        daily_expenses_median = statistics.median(daily_expenses_array)
        daily_expenses_mean = statistics.mean(daily_expenses_array)
        daily_expenses_mode = statistics.mode(daily_expenses_array)
        # print(daily_expenses_array)
        stats.update({'daily_expenses_mean': int(daily_expenses_mean)})
        stats.update({'daily_expenses_median': int(daily_expenses_median)})
        stats.update({'daily_expenses_mode': int(daily_expenses_mode)})
        stats.update({'daily_expenses': daily_expenses_array})
        stats.update({'daily_income': daily_income_array})
        stats.update({'dates_array': dates_array})
        # get last element and set to today's income and today's date
        stats.update({'today_expenses': daily_expenses_array[-1]})
        stats.update({'today_date': dates_array[-1]})
        return stats


@login_required(login_url='/admin/login/')
def home(request):
    form = forms.IncomeExpenseCreationForm
    form_set_expenses = formset_factory(forms.IncomeExpenseCreationForm, extra=6)
    form_set_income = formset_factory(forms.IncomeExpenseCreationForm, extra=6)
    form_set_schedule = formset_factory(forms.SchedulerForm, extra=6)
    form_set_periodic_expenses = formset_factory(forms.PeriodicExpensesForm, extra=6)
    incomeAndExpense = models.IncomeAndExpense.objects.all()
    today = datetime.date.today()
    schedule = models.Scheduler.objects.all().filter(date__gte=today)
    periodic_expense = models.PeriodicExpense.objects.all()
    total_periodic_cost = models.PeriodicExpense.objects.all().aggregate(Sum('amount')).get('amount__sum') or 0
    # print(schedule)

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
        'periodic_expense': periodic_expense,
        'form_set_expenses': form_set_expenses,
        'form_set_income': form_set_income,
        'form_set_periodic_expenses': form_set_periodic_expenses,
        'bank_balance': bank_balance,
        'cash_balance': cash_balance,
        'total': total,
        'stats': stats,
        'form_set_schedule': form_set_schedule,
        'schedule': schedule,
        'total_periodic_cost': total_periodic_cost,
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


@login_required(login_url='/admin/login/')
def schedule_create_formset(request):
    if request.method == 'POST':
        ScheduleCreateFormset = formset_factory(forms.SchedulerForm)
        form_set = ScheduleCreateFormset(request.POST or None)
        if form_set.is_valid():
            for form in form_set:
                if form.cleaned_data != {}:
                    form.save(commit=True)

        return redirect('/')


@login_required(login_url='/admin/login/')
def periodic_expenses_create_formset(request):
    if request.method == 'POST':
        PeriodicExpensesCreateFormset = formset_factory(forms.PeriodicExpensesForm)
        form_set = PeriodicExpensesCreateFormset(request.POST or None)
        if form_set.is_valid():
            for form in form_set:
                if form.cleaned_data != {}:
                    form.save(commit=True)

        return redirect('/')


# @login_required(login_url='/admin/login/')
# AJAX
def send_transaction_in_json(request):
    date_requested = parse(request.GET.get('date'))
    print(date_requested)
    requested_day_trans = models.IncomeAndExpense.objects.filter(date=date_requested)
    transactions = serializers.serialize("json", requested_day_trans)
    # print(transactions)
    return HttpResponse(json.dumps(transactions), content_type="application/json")


# Todo Incomplete function
def login_user(request):
    pass


def logout_user(request):
    pass
