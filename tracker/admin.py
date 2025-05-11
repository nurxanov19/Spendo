from django.contrib import admin
from .models import IncomeCategory, ExpenseCategory, Account, Income,Expense

admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(ExpenseCategory)
admin.site.register(Account)
admin.site.register(IncomeCategory)



