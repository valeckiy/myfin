from django.contrib import admin

from .models import Wallets, Ballance, Categories, Transactions

# admin.site.register(Wallets)
admin.site.register(Ballance)
admin.site.register(Categories)
admin.site.register(Transactions)

class WalletsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

# Register the admin class with the associated model
admin.site.register(Wallets, WalletsAdmin)
