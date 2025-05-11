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



class AddCategory(View):
    def get(self, request):
        income_categories = IncomeCategory.objects.all()
        expense_categories = ExpenseCategory.objects.all()
        inc_form = AddIncomeCategoryForm()
        exp_form = AddExpenseCategoryForm()
        return render(request, 'main.html', {'inc_cat': income_categories, 'exp_cat': expense_categories,
                                             'inc_form': inc_form,
        'exp_form': exp_form})

    def post(self, request):
        form_type = request.POST.get('form_type')

        if form_type == 'income':
            exp_form = AddExpenseCategoryForm(request.POST)
            inc_form = AddIncomeCategoryForm(request.POST)
            if inc_form.is_valid():
                inc_form.save()
                return redirect('main')
        elif form_type == 'expense':
            exp_form = AddExpenseCategoryForm(request.POST)
            inc_form = AddIncomeCategoryForm(request.POST)
            if exp_form.is_valid():
                exp_form.save()
                return redirect('main')

        context = {'inc_form': inc_form, 'exp_form': exp_form}
        return render(request, 'main.html', context)


class AddAccount(View):
    def get(self, request):
        form = AddIncomeCategoryForm()
        accounts = Account.object.filter(user=request.user)

        return render(request, 'main.html', {'form': form, 'accounts': accounts})

    def post(self, request):
        form = AddAccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('main')
        return render(request, 'main.html', {'form': form})


def get_context( request, extra_context=None):
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
        monthly_expense = Expense.objects.filter( user=request.user, created_at__gte=month_start,created_at__lt=month_end
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        expense_data.append(float(monthly_expense) if monthly_expense else 0)

    context = {'income': income, 'expense': expense, 'total_income': float(total_income), 'total_expense': float(total_expense),
        'total_balance': float(total_balance), 'expense_data': expense_data, }

    if extra_context:
        context.update(extra_context)
    return context


class ListIncomeExpenseView(View):
    def get(self, request):
        return render(request, 'main.html', get_context( request))


class AddIncomeExpenseView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'main'

    def get(self, request):
        context = get_context(request, {'income_form': AddIncomeForm(),
            'expense_form': AddExpenseForm()})

        return render(request, 'main.html', context)

    def post(self, request):
        income_form = AddIncomeForm(request.POST)
        expense_form = AddExpenseForm(request.POST)
        if 'income' in request.POST and income_form.is_valid():
            income = income_form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('main')
        elif 'expense' in request.POST and expense_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('main')
        context = get_context(request, {
            'income_form': income_form,
            'expense_form': expense_form,
            'show_income_modal': 'income' in request.POST and not income_form.is_valid(),
            'show_expense_modal': 'expense' in request.POST and not expense_form.is_valid(),
        })
        return render(request, 'main.html', context)


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

