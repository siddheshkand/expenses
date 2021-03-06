from django.conf.urls.static import static
from django.urls import path, include
# from expenses import settings
from django.conf import settings
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.DefaultRouter()
router.register('income_and_expenses_rest', views.IncomeAndExpenseViewSet)

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('get/transaction/', views.send_transaction_in_json, name='send_transaction'),
    path('expense/create/multiple/', views.expenses_create_formset, name='expense_create_multiple'),
    path('income/create/multiple/', views.income_create_formset, name='income_create_multiple'),
    path('schedule/create/multiple/', views.schedule_create_formset, name='schedule_create_multiple'),
    path('periodic_expenses/create/multiple/', views.periodic_expenses_create_formset,
         name='periodic_expenses_create_multiple'),
    path('rest/', include(router.urls)),
    path('auth/', obtain_auth_token)
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
