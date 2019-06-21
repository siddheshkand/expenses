from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('expense/create/multiple/', views.expenses_create_formset, name='expense_create_multiple'),
    path('income/create/multiple/', views.income_create_formset, name='income_create_multiple')
]
