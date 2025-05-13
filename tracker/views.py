from django.core.signals import request_started
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Income, IncomeCategory, ExpenseCategory, Expense, Account
from .forms import AddIncomeForm, AddExpenseForm, AddIncomeCategoryForm, AddExpenseCategoryForm, AddAccountForm
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone
import json


def get_context(request, extra_context=None):
    income = Income.objects.filter(user=request.user)
    expense = Expense.objects.filter(user=request.user)

    total_income = income.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expense.aggregate(Sum('amount'))['amount__sum'] or 0
    total_balance = total_income - total_expense

    end_date = timezone.now()
    start_date = end_date - timedelta(days=180)
    expense_data = []

    for i in range(6):
        month_start = start_date + timedelta(days=30 * i)
        month_end = month_start + timedelta(days=30)
        monthly_expense = \
        Expense.objects.filter(user=request.user, created_at__gte=month_start, created_at__lt=month_end
                               ).aggregate(Sum('amount'))['amount__sum'] or 0

        expense_data.append(float(monthly_expense) if monthly_expense else 0)

    context = {'income': income, 'expense': expense, 'total_income': float(total_income),
               'total_expense': float(total_expense),
               'total_balance': float(total_balance), 'expense_data': expense_data, }

    if extra_context:
        context.update(extra_context)
    return context


class DashboardView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'main'

    def get(self, request):
        context = get_context(request)
        return render(request, 'dashboard.html', context)


class AddCategory(View):
    def get(self, request):
        form_type = request.GET.get('type', 'income')
        form = AddIncomeCategoryForm(user=request.user) if form_type == 'income' else AddExpenseCategoryForm(user=request.user)
        return render(request, 'add_category.html', {'form': form, 'form_type': form_type})

    def post(self, request):
        form_type = request.POST.get('form_type')
        form = AddIncomeCategoryForm(request.POST, user=request.user) if form_type == 'income' else AddExpenseCategoryForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('main')
        return render(request, 'add_category.html', {'form': form, 'form_type': form_type})


class AddAccount(View):
    def get(self, request):
        form = AddAccountForm()
        return render(request, 'add_account.html', {'form': form})

    def post(self, request):
        form = AddAccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()

            if account.balance > 0:
                initial_category, _ = IncomeCategory.objects.get_or_create(name="Initial Balance", user=request.user)
                Income.objects.create(
                    user=request.user,
                    account=account,
                    amount=account.balance,
                    type="Initial Balance",
                    category=initial_category
                )
            return redirect('main')
        return render(request, 'add_account.html', {'form': form})



class AddIncomeExpenseView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'main'

    def get(self, request):
        type_param = request.GET.get('type', 'income')
        form = AddIncomeForm(user=request.user) if type_param == 'income' else AddExpenseForm(user=request.user)
        return render(request, 'add_income_expense.html', {'form': form, 'type': type_param})

    def post(self, request):
        type_param = request.POST.get('type')
        form = AddIncomeForm(request.POST, user=request.user) if type_param == 'income' else AddExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            if obj.account:
                if isinstance(obj, Expense):
                    obj.account.balance -= obj.amount
                elif isinstance(obj, Income):
                    obj.account.balance += obj.amount
                obj.account.save()
            return redirect('main')
        return render(request, 'add_income_expense.html', {'form': form, 'type': type_param})


class ReportsView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'main'

    def get(self, request):
        date_range = request.GET.get('range', '30days')
        if date_range == '7days':
            days = 7
        elif date_range == '90days':
            days = 90
        else:
            days = 30

        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)

        income = Income.objects.filter(user=request.user, created_at__gte=start_date, created_at__lte=end_date)
        expenses = Expense.objects.filter( user=request.user,  created_at__gte=start_date,created_at__lte=end_date)

        total_income = sum(inc.amount for inc in income) or 0
        total_expense = sum(exp.amount for exp in expenses) or 0
        bar_labels = ['Income', 'Expenses']
        bar_data = [float(total_income), float(total_expense)]

        pie_labels = []
        pie_data = []

        categories = {}
        for exp in expenses:
            category_name = exp.category.name
            if category_name not in categories:
                categories[category_name] = 0
            categories[category_name] += float(exp.amount)

        for category_name, amount in categories.items():
            pie_labels.append(category_name)
            pie_data.append(amount)

        context = {
            'bar_chart_data': json.dumps({'labels': bar_labels, 'data': bar_data}),
            'pie_chart_data': json.dumps({'labels': pie_labels, 'data': pie_data}), 'selected_range': date_range }

        return render(request, 'reports.html', context)



'''
-- aggregate() -> bu Djanog ORM metodi bo'lib, hisob-kitob amallarini bajaradi, masalan (sum, max, min, average), u doim dect obyekt qaytaradi
-- SUM -> bu tegishli databaza malumotlarini berilgan field bo'yicha qo'shib chiqaradi  --> Income.objects.filter(user=request.user).aggregate(Sum('amount')) --> {'amount__sum': 500.00}
-- 'amount__sum' -> bu esa Djangodagi format usuli, ya'ni {field}__{function}

    Bu yerda ishlatilayotgan logika oyalrni 180 ni 6 ga bo'ladi yani har bir oy uchun 30 kundan

'''


