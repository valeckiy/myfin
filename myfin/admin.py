from django.contrib import admin

from .models import Wallets, Ballance, Categories, Transactions

class WalletsAdmin(admin.ModelAdmin):
    list_display = ('name', 'currency')
    list_filter = ('currency',)     
    
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction') 
    list_filter = ( 'direction',) 
    
class BallanceAdmin(admin.ModelAdmin):
    list_display = ('id_wallet', 'total')  
    
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('id_wallet', 'suma', 'category', 'date')   
    

# Register the admin class with the associated model
admin.site.register(Wallets, WalletsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Ballance,BallanceAdmin)
admin.site.register(Transactions,TransactionsAdmin)