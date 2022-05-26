from django.contrib import admin

from .models import Wallets, Ballance, Categories, Exchanges,Transactions,Profile

class WalletsAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'currency','image', 'user')
    list_filter = ('currency', 'user')     
    
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'direction', 'user','image','hidden') 
    list_filter = ( 'direction', 'user') 
    
class BallanceAdmin(admin.ModelAdmin):
    list_display = ('id','id_wallet', 'total')  
    
class ExchangesAdmin(admin.ModelAdmin):
    list_display = ('id','id_wallet_from','id_wallet_to', 'suma_from', 'suma_to', 'course', 'date')  
    
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('id','id_wallet', 'suma', 'category', 'date', 'id_exchange')      
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','currency')      
    

# Register the admin class with the associated model
admin.site.register(Wallets, WalletsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Ballance,BallanceAdmin)
admin.site.register(Exchanges,ExchangesAdmin)
admin.site.register(Transactions,TransactionsAdmin)
admin.site.register(Profile,ProfileAdmin)