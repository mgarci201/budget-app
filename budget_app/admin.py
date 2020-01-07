from django.contrib import admin
from .models import AccountInfo, ExpenseInfo

# Register your models here.
admin.site.register(AccountInfo)
admin.site.register(ExpenseInfo)