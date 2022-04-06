from django.contrib import admin

from .models import Wallets, Ballance, Categories, Transactions

admin.site.register(Wallets)
admin.site.register(Ballance)
admin.site.register(Categories)
admin.site.register(Transactions)
