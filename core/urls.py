# dbank/core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create_account/', views.create_account, name='create_account'),
    #path('account/create/', views.create_account, name='create_account'),
    #path('account/<int:account_id>/', views.account_details, name='account_details'),
    #path('account/<int:account_id>/deposit/', views.deposit, name='deposit'),
    #path('account/<int:account_id>/withdraw/', views.withdraw, name='withdraw'),
]
