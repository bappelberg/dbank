# dbank/core/forms.py
from django import forms
from .models import User, Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'balance']

    account_type = forms.ChoiceField(choices=[('private', 'Private'), ('savings', 'Savings')])
    balance = forms.DecimalField(max_digits=10, decimal_places=2)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password'])
            user.save()
        return user
