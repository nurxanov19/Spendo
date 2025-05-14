from rest_framework.serializers import ValidationError
from rest_framework import serializers
from tracker.models import Income, Expense, IncomeCategory, ExpenseCategory, Account


class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = ['name']

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['name']

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

class AccountSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=50)
    type_choice = serializers.ChoiceField(choices=Account.TYPE_CHOICES)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)

    class Meta:
        model = Account
        fields = ['type', 'type_choice', 'balance']

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['amount', 'account', 'category']

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        if attrs.get('account') and attrs['account'].user != self.context['request'].user:
            raise ValidationError("Invalid account")
        if attrs.get('category') and attrs['category'].user != self.context['request'].user:
            raise ValidationError("Invalid category")
        return attrs

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['amount', 'account', 'category']

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        if attrs.get('account') and attrs['account'].user != self.context['request'].user:
            raise ValidationError("Invalid account")
        if attrs.get('category') and attrs['category'].user != self.context['request'].user:
            raise ValidationError("Invalid category")
        return attrs