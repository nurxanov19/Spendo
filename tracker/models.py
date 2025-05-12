from django.db import models

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'expensecategory'
        verbose_name_plural = 'expensecategories'

    def __str__(self):
        return self.name


class IncomeCategory(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'incomecategory'
        verbose_name_plural = 'incomecategories'

    def __str__(self):
        return self.name


class Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    TYPE_CHOICES = [('cash', 'Cash'), ('card', 'Card')]
    type_choice = models.CharField(max_length=20, choices=TYPE_CHOICES)
    type = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        try:
            return f"{self.user.username} - {self.type} ({self.type_choice})"
        except:
            return f"Account {self.id} - {self.type} ({self.type_choice})"



class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.amount} to {self.account}"


class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.amount} to {self.account}"

