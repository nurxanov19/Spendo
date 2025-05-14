from django.urls import path
from .views import DashboardViewApi, AddAccountApi, AddCategoryApi, AddIncomeExpenseApi, ReportsViewApi

urlpatterns = [
    path('dashboard/', DashboardViewApi.as_view(), name='dashboard'),
    path('categories/', AddCategoryApi.as_view(), name='add_category'),
    path('accounts/', AddAccountApi.as_view(), name='add_account'),
    path('transactions/', AddIncomeExpenseApi.as_view(), name='add_income_expense'),
    path('reports/', ReportsViewApi.as_view(), name='reports'),

]