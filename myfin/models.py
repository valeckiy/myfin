from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
 
class Wallets(models.Model):
    name = models.CharField(max_length=45)
    currency = models.CharField(max_length=45)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.CharField(max_length=45)
    
class Ballance(models.Model):
    id_wallet = models.IntegerField()
    total = models.DecimalField(max_digits=12, decimal_places=2)   
    
    
class Categories(models.Model):
    name = models.CharField(max_length=45)
    direction = models.CharField(max_length=45)      
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    hidden = models.BooleanField(null=False, blank=False,default=True)
    dop_cat_id = models.IntegerField()
    image = models.CharField(max_length=45)
  
class Exchanges(models.Model):
    id_wallet_from =models.IntegerField()
    id_wallet_to = models.IntegerField()
    suma_from = models.DecimalField( max_digits=12, decimal_places=2)  
    suma_to = models.DecimalField( max_digits=12, decimal_places=2)  
    course = models.DecimalField( max_digits=12, decimal_places=4)  
    date = models.DateTimeField()  
        
class Transactions(models.Model):
    id_wallet = models.IntegerField()
    suma = models.DecimalField( max_digits=12, decimal_places=2)  
    category = models.IntegerField()   
    date = models.DateTimeField()  
    id_exchange = models.ForeignKey(Exchanges,on_delete=models.CASCADE, null=True, blank=True )
    comment = models.TextField(null=True, blank=True,default='')
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=45)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  
   
    

  