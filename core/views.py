# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import AccountForm, UserForm
from .models import Account, User
from django.http import HttpResponse

def home(request):
    return render(request, 'core/home.html')

def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('account_list')
    else:
        form = AccountForm()
    return render(request, 'core/create_account.html', {'form': form})


def account_details(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.user != account.user:
        return redirect('home')
    return render(request, 'core/account_details.html', {'account': account})


def deposit(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            account.deposit(amount)
            messages.success(request, f"Deposited {amount} to account")
        except ValidationError as e:
            messages.error(request, str(e))
        return redirect('account_details', account_id=account.id)
    return render(request, 'core/deposit.html', {'account': account})


def withdraw(request, account_id):
    """Ta ut pengar från konto"""
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            account.withdraw(amount)
            messages.success(request, f"Withdrew {amount} from account")
        except ValidationError as e:
            messages.error(request, str(e))
        return redirect('account_details', account_id=account.id)
    return render(request, 'core/withdraw.html', {'account': account})

