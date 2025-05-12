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
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)
        self.fields['category'].queryset = IncomeCategory.objects.filter(user=user)



class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'account', 'category']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': '$0.00'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)
        self.fields['category'].queryset = ExpenseCategory.objects.filter(user=user)



class AddIncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = ['name',]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        category = super().save(commit=False)
        category.user = self.user
        if commit:
            category.save()
        return category


class AddExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name',]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        category = super().save(commit=False)
        category.user = self.user
        if commit:
            category.save()
        return category


class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['type_choice', 'type', 'balance']
        widgets = {
            'type_choice': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter account name (ex: Humo, Cash wallet)'}),
            'balance': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Initial balance'}),
        }
