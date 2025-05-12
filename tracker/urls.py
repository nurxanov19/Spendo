from django.urls import path
from .views import AddIncomeExpenseView, ReportsView, AddCategory, AddAccount, DashboardView,  ReportsView ,switch_language




urlpatterns = [
    path('', DashboardView.as_view(), name='main'),
    path('add-account/', AddAccount.as_view(), name='add-account'),
    path('add-category/', AddCategory.as_view(), name='add_category'),
    path('add-income-expense/', AddIncomeExpenseView.as_view(), name='add_income_expense'),
    path('reports/', ReportsView.as_view(), name='reports'),
path('switch-language/<str:language_code>/', switch_language, name='switch_language'),
]

