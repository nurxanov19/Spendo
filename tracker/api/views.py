from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta

from tracker.api.serializers import IncomeCategorySerializer, ExpenseCategorySerializer, AccountSerializer, \
    IncomeSerializer, ExpenseSerializer
from tracker.models import Income, Expense, IncomeCategory, ExpenseCategory, Account
import json



class DashboardViewApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
            monthly_expense = Expense.objects.filter(user=request.user,created_at__gte=month_start,created_at__lt=month_end).aggregate(Sum('amount'))['amount__sum'] or 0
            expense_data.append(float(monthly_expense))

        return Response({'message': 'Dashboard data retrieved',
                'data': {'total_income': float(total_income), 'total_expense': float(total_expense),
                    'total_balance': float(total_balance),'expense_data': expense_data}}, status=status.HTTP_200_OK)


class AddCategoryApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form_type = request.data.get('type', 'income')
        serializer_class = IncomeCategorySerializer if form_type == 'income' else ExpenseCategorySerializer
        serializer = serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': ' category created '},
                            status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class AddAccountApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AccountSerializer,
        responses={
            201: openapi.Response('Account created', AccountSerializer),
            400: 'Bad Request'
        })

    def post(self, request):
        serializer = AccountSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            account = serializer.save()
            if account.balance > 0:
                initial_category, _ = IncomeCategory.objects.get_or_create(name="Initial Balance", user=request.user)
                Income.objects.create(user=request.user, account=account,
                                      amount=account.balance, type="Initial Balance", category=initial_category)
            return Response({'message': f'Account created '},status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class AddIncomeExpenseApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        type_param = request.data.get('type', 'income')
        serializer_class = IncomeSerializer if type_param == 'income' else ExpenseSerializer
        serializer = serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            obj = serializer.save()
            if obj.account:
                if isinstance(obj, Expense):
                    obj.account.balance -= obj.amount
                elif isinstance(obj, Income):
                    obj.account.balance += obj.amount
                obj.account.save()
            return Response({'message': f'{type_param} added'},status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class ReportsViewApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_range = request.query_params.get('range', '30days')
        days = {'7days': 7, '90days': 90}.get(date_range, 30)
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)

        income = Income.objects.filter(user=request.user, created_at__gte=start_date, created_at__lte=end_date)
        expenses = Expense.objects.filter(user=request.user, created_at__gte=start_date, created_at__lte=end_date)
        total_income = sum(inc.amount for inc in income) or 0
        total_expense = sum(exp.amount for exp in expenses) or 0

        bar_labels = ['Income', 'Expenses']
        bar_data = [float(total_income), float(total_expense)]

        categories = {}
        for exp in expenses:
            category_name = exp.category.name
            categories[category_name] = categories.get(category_name, 0) + float(exp.amount)

        pie_labels = list(categories.keys())
        pie_data = list(categories.values())

        return Response({'message': 'Reports data retrieved','data': {'bar_chart': {'labels': bar_labels, 'data': bar_data},
                    'pie_chart': {'labels': pie_labels, 'data': pie_data},
                    'selected_range': date_range }}, status=status.HTTP_200_OK)