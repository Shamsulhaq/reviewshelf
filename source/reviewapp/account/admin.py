from django.contrib import admin
from .models import User,BalanceHistory

admin.site.register(User)
admin.site.register(BalanceHistory)