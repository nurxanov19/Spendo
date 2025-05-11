from django import forms
from .models import Income, Expense, IncomeCategory, ExpenseCategory, Account


from django import forms
from .models import Income, Expense

class AddIncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'account', 'category']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': '$0.00'}),

        }

class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'account', 'category']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': '$0.00'}),

        }


class AddIncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = ['name',]


class AddExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name',]


class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['type_choice', 'type', 'balance']
        widgets = {
            'type_choice': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter account name (ex: Humo, Cash wallet)'}),
            'balance': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Initial balance'}),
        }
