from django.urls import path, include
from .views import AddIncomeExpenseView, ReportsView, AddCategory, AddAccount, DashboardView,  ReportsView




urlpatterns = [
    path('', DashboardView.as_view(), name='main'),
    path('add-account/', AddAccount.as_view(), name='add-account'),
    path('add-category/', AddCategory.as_view(), name='add_category'),
    path('add-income-expense/', AddIncomeExpenseView.as_view(), name='add_income_expense'),
    path('reports/', ReportsView.as_view(), name='reports'),
    #path('i18n/', include('django.conf.urls.i18n')),
]

