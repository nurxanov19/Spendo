from django.urls import path
from .views import AddIncomeExpenseView, ListIncomeExpenseView, ReportsView, AddCategory, AddAccount



urlpatterns = [
    path('', ListIncomeExpenseView.as_view(), name='main'),
    path('add/', AddIncomeExpenseView.as_view(), name='add_income_expense'),
    path('reports/', ReportsView.as_view(), name='reports'),
    path('add-category/', AddCategory.as_view(), name='add_category'),
    path('add-account/', AddAccount.as_view(), name='add-account'),
]