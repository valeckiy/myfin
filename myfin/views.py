from django.db import connection
from django.shortcuts import render
from django.http import HttpResponseRedirect
from datetime import datetime
from .db import DB

 
# get wallets from bd 
def index(request):
    cursor = connection.cursor()
    if request.method == "POST":
        actions = request.POST.get("actions")
        id = int(request.POST.get("id"))
        if actions == 'wallet_delete' and id > 0:
            DB.del_wallet(cursor,id)
            return HttpResponseRedirect('/')
        elif actions == 'transaction_delete' and id > 0:
           
            try:
                sum_transaction = -int(request.POST.get("sum_transaction"))
                id_wallet = int(request.POST.get("id_wallet"))
            except:
                sum_transaction = 0
                id_wallet = 0
         
            DB.update_ballance(id_wallet,sum_transaction)
            DB.del_trancaction(id)
            return HttpResponseRedirect('/')
        
        elif actions == 'transaction_add':
            try:
                sum_transaction = int(request.POST.get("sum_transaction"))
                category_id = request.POST.get("category")
            except:
                sum_transaction = 0
                category_id = 0
            
            if sum_transaction != 0:
                direction_transaction = DB.direction_transaction_for_category(cursor,category_id) 
                sum_transaction = sum_transaction * int(direction_transaction)
                
                DB.add_transaction(id,sum_transaction,category_id)
                DB.update_ballance(id,sum_transaction)
                
                return HttpResponseRedirect('/')
     
    el_categories = DB.list_categories(cursor)    
    el_wallets = DB.list_wallets(cursor)
    
    time = datetime.now()
    date_start = time.strftime("%Y-%m-01")
    date_end = time.strftime("%Y-%m-%d")
    
    el_transaction = DB.list_transaction(cursor,date_start,date_end,5,0) 
   
    return render(request, "index.html", {"el_wallets": el_wallets,"el_categories": el_categories,"el_transaction": el_transaction})


# add wallet 
def add_wallet(request):
    if request.method == "POST":
        cursor = connection.cursor()
        name = request.POST.get("wallet_name")
        currency = request.POST.get("currency")
        total = request.POST.get("ballance")
        data_return = DB.add_wallet(cursor,name,currency,total)
        return HttpResponseRedirect('/')
        
    return render(request, "add_wallet.html")
 

# add wallet  result
def add_wallet_results(request):
    if request.method == "POST":
        cursor = connection.cursor()
        name = request.POST.get("wallet_name")
        currency = request.POST.get("currency")
        total = request.POST.get("ballance")
        data = DB.add_wallet(cursor,name,currency,total)
      
    return render(request, "add_wallet_results.html",context=data)

# categories
def categories(request):
     cursor = connection.cursor()
     
     if request.method == "POST":
         
         actions = request.POST.get("actions")
         id = int(request.POST.get("id"))
         
         if actions == 'category_add':
             name = request.POST.get("category_name")
             direction = request.POST.get("category_direction")
             DB.add_categories(cursor,name,direction)     
             return HttpResponseRedirect('/categories')
         
         elif actions == 'category_delete'and id > 0:
             DB.del_categories(cursor,id)
             return HttpResponseRedirect('/categories')  
         
         elif actions == 'category_edit' and id > 0:
             category_name = request.POST.get("category_name")
             category_direction = request.POST.get("category_direction")
             DB.edit_categories(cursor,id,category_name,category_direction)
             return HttpResponseRedirect('/categories')             

     el_categories = DB.list_categories(cursor)
     return render(request, "categories.html", {"el_categories": el_categories})

# edit categories
def edit_categories(request):
         if request.method == "POST":
             the_id = int(request.POST.get("id"))
             the_name = request.POST.get("name")
             the_direction = request.POST.get("direction")            
         return render(request, "edit_categories.html", {"the_id": the_id,"the_name": the_name,"the_direction": the_direction})
     
        
# transaction
def transaction(request):
    cursor = connection.cursor()
    if request.method == "POST":
         actions = request.POST.get("actions")
         id = int(request.POST.get("id"))
         if actions == 'transaction_add':
             sum_transaction = int(request.POST.get("sum_transaction"))
             category_id = request.POST.get("category")
             
             DB.add_transaction(id,sum_transaction,category_id)
             DB.update_ballance(id,sum_transaction)         
      
             return HttpResponseRedirect('/transaction')
         
         elif actions == 'transaction_delete'and id > 0:
             id_wallet = int(request.POST.get("id_wallet"))
             sum_transaction = int(request.POST.get("sum_transaction"))
             DB.update_ballance(id_wallet,sum_transaction)
             DB.del_trancaction(id)
             return HttpResponseRedirect('/transaction')  
         elif actions == 'transaction_edit' and id > 0:
             """category_name = request.POST.get("category_name")
             category_direction = request.POST.get("category_direction")
             edit_c = Categories.objects.get(pk=id)
             edit_c.name = category_name
             edit_c.direction = category_direction
             edit_c.save()
             return HttpResponseRedirect('/transaction')    """         
    time = datetime.now()
    date_start = time.strftime("%Y-%m-01")
    date_end = time.strftime("%Y-%m-%d")
    
    try:
        filtr_id_wallet = int(request.POST.get("id_wallet"))
        filtr_id_category = int(request.POST.get("id_category"))
        filtr_date_start = request.POST.get("date_start")
        filtr_date_end = request.POST.get("date_end")
    except:
        filtr_id_wallet = 0 
        filtr_id_category = 0
        filtr_date_start = date_start
        filtr_date_end = date_end
      
        
    el_transaction = DB.list_transaction(cursor,filtr_date_start,filtr_date_end,500,filtr_id_wallet,filtr_id_category) 
    el_wallets = DB.list_wallets(cursor)
    el_categories = DB.list_categories(cursor)

    return render(request, "transaction.html", {"el_transaction": el_transaction,"el_wallets": el_wallets
                                                ,"el_categories": el_categories,"date_start": filtr_date_start
                                                ,"date_end": filtr_date_end,"filtr_id_wallet": filtr_id_wallet
                                                ,"filtr_id_category": filtr_id_category})     