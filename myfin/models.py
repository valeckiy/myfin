from django.db import models
 
class Wallets(models.Model):
    name = models.CharField(max_length=45)
    currency = models.CharField(max_length=45)
    
class Ballance(models.Model):
    id_wallet = models.IntegerField()
    total = models.DecimalField(max_digits=12, decimal_places=2)    
    
class Categories(models.Model):
    name = models.CharField(max_length=45)
    direction = models.CharField(max_length=45)      
    
class Transactions(models.Model):
    id_wallet = models.IntegerField()
    suma = models.DecimalField( max_digits=12, decimal_places=2)  
    category = models.IntegerField()   
    date = models.DateTimeField()  