# dbank/core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import random
import string


def generate_account_number():
    """Generates a random account number"""
    return ''.join(random.choices(string.digits, k=10))  # Exempel på ett 10-siffrigt kontonummer


class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # Fixes SystemCheckError
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.username


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=[('private', 'Private'), ('savings', 'Savings')])
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_number = models.CharField(max_length=20, unique=True, default=generate_account_number)

    def __str__(self):
        return f'Account {self.account_number} ({self.user.username})'

    def deposit(self, amount):
        """Deposits to account"""
        if amount <= 0:
            raise ValidationError("Deposit amount must be positive")
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        """Withdraw from account"""
        if amount <= 0:
            raise ValidationError("Withdraw amount must be positive")
        if amount > self.balance:
            raise ValidationError("Insufficient funds")
        self.balance -= amount
        self.save()


class Transaction(models.Model):
    sender_account = models.ForeignKey(Account, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver_account = models.ForeignKey(Account, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction from {self.sender_account.account_number} to {self.receiver_account.account_number} of {self.amount}"
