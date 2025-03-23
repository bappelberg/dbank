# dbank/urls.py

from django.contrib import admin
from django.urls import path, include
from core.views import home, create_account
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('create_account/', create_account, name='create_account'),
    path('', home, name='home'),  # To show home site on root URL
]
