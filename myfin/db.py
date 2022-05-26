
from collections import namedtuple
from .models import Wallets,Ballance,Transactions,Categories,Exchanges,Profile
from datetime import datetime,timedelta

class DB:
    

    def namedtuplefetchall(cursor):
        "Return all rows from a cursor as a namedtuple"
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]

    #WALLETS
    
    
    def list_wallets(cursor,request):
        user_id=request.user.id
        SQL = """ select  w.name,b.total, w.currency, w.id, w.image from myfin_wallets as w 
               left join myfin_ballance as b on b.id_wallet=w.id where user_id=(%s) order by name """
        cursor.execute(SQL,(user_id,))
        return DB.namedtuplefetchall(cursor)
    
    
    def add_wallet(cursor, name, currency, ballance,image,request):
        user_id=request.user.id
        
        if image=='':
            image = 'blank.png'
            
        new_w = Wallets()
        new_w.name = name
        new_w.currency = currency
        new_w.image = image
        new_w.user_id = user_id
        new_w.save()
    
        max_id = Wallets.objects.all().last().id
        total = ballance
        
        category_id = DB.GetAddDopCategory(1,'ballance')
        
        DB.add_transaction(max_id, total, category_id)
        DB.add_ballance(max_id, total)
    
        return {"name": new_w.name, "currency": new_w.currency, "total": total}
    
    def get_wallet_currancy(id):
        wallet_list = Wallets.objects.all().filter(id=id)
        return wallet_list[0].currency
    
    def edit_wallet(cursor, id,name, currency, image,request):
        if image=='':
            image = 'blank.png'
        edit_w = Wallets.objects.get(pk=id)
        edit_w.name = name
        edit_w.currency = currency
        edit_w.image = image
        edit_w.save()        
        
        return {"name": edit_w.name, "currency": edit_w.currency}
    
    def del_wallet(cursor, id):
        Wallets.objects.filter(id=id).delete()
        
        all_row = Transactions.objects.filter(id_wallet=id).all() 
        for w_row in all_row:
            DB.del_transaction(w_row.id)

    
    #CATEGORIES
    
    
    def list_categories(cursor,request,direction=""):
        if direction=="":
            return Categories.objects.all().filter(user=request.user,hidden=False).order_by("direction","name")
        else:
            return Categories.objects.all().filter(user=request.user,direction=direction,hidden=False).order_by("direction","name")
    
    
    def add_categories(cursor, name, direction,image,request,hidden=False,dop_cat_id=0):
        if image=='':
            image = 'blank.png'
        user_id=request.user.id
        new_c = Categories()
        new_c.name = name
        new_c.direction = direction
        new_c.image = image
        new_c.user_id = user_id
        new_c.hidden = hidden
        new_c.dop_cat_id = dop_cat_id
        new_c.save()
    
    
    def edit_categories(cursor, id, name, direction,image):
        if image=='':
            image = 'blank.png'
        edit_c = Categories.objects.get(pk=id)
        edit_c.name = name
        edit_c.image = image
        edit_c.direction = direction
        edit_c.save()
    
    
    def del_categories(cursor, id):
        Categories.objects.filter(id=id).delete()
    
    #TRANSACTION
   
    def direction_transaction_for_category(cursor,id_category) -> None:
        """ select direction transaction for id category in DB """
            
        SQL = """select  direction 
                     from myfin_categories WHERE id=(%s) limit 1 """
        cursor.execute(SQL, (id_category,))

        row_one =  cursor.fetchone ()

        if  row_one is None:
            return 1
        elif  row_one[0] == 'Profit':
            return 1
        else:            
            return -1  
    
    def list_transaction(cursor, request,date_start,date_end,limit=100, filtr_id_wallet=0,filtr_id_category=0,filtr_currency="0"):
        """ select transaction from DB"""
        user_id=request.user.id
        date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
        date_end = datetime.strptime(date_end, "%Y-%m-%d").date()+timedelta(days=1)
        SQL = """ select  t.date,t.comment, w.name as wallet, c.name as category, t.suma,
              w.currency,t.id,w.id as id_wallet, c.image as image, w.image as image_wallet
              from myfin_transactions as t
              left join myfin_categories as c on c.id = t.category
              left join myfin_wallets as w on w.id = t.id_wallet 
              where (t.date>=%s and t.date<%s) and(w.id=%s or %s=0)and(t.category=%s or %s=0) 
              and(w.currency=%s or %s="0")
              and w.user_id=(%s)
              order by t.date DESC limit %s """
        cursor.execute(SQL, (date_start,date_end,filtr_id_wallet, filtr_id_wallet
                             , filtr_id_category,filtr_id_category,filtr_currency,filtr_currency,user_id,limit,))
        return DB.namedtuplefetchall(cursor)
    
    def list_transaction_group_category(cursor, request,date_start,date_end,direction="cost",filtr_currency=""):
        """ select transaction from DB"""
        user = request.user
        user_id=user.id
        if filtr_currency=="":
            filtr_currency = DB.GetCurrancyUser(user)    
        
        if direction=="cost":
            t_sum = "0"
            t_sum2 = "-1000000000"
            sort = 1
        else:
            t_sum = "1000000000000"
            t_sum2 = "0"
            sort = -1
            
        date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
        date_end = datetime.strptime(date_end, "%Y-%m-%d").date() +timedelta(days=1)   
            
        SQL = """ select  c.name as category,c.image as image,w.currency, SUM(t.suma) as suma              
              from myfin_transactions as t
              left join myfin_categories as c on c.id = t.category
              left join myfin_wallets as w on w.id = t.id_wallet 
              where t.suma<%s and t.suma>%s and (t.date>=%s and t.date<%s)  and w.currency=%s  
              and w.user_id=(%s) group by c.name order by SUM(t.suma*%s) """
        cursor.execute(SQL, (t_sum,t_sum2,date_start,date_end, filtr_currency, user_id,sort,))
        return DB.namedtuplefetchall(cursor)
    
    def list_transaction_group_currancy(cursor, request,date_start,date_end):
        """ select transaction from DB"""
        user_id=request.user.id
        date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
        date_end = datetime.strptime(date_end, "%Y-%m-%d").date()+timedelta(days=1)
        SQL = """ select  w.currency as currency, t.suma              
              from myfin_transactions as t
              left join myfin_categories as c on c.id = t.category
              left join myfin_wallets as w on w.id = t.id_wallet 
              where t.suma<0 and (t.date>=%s and t.date<%s) 
              and w.user_id=(%s) group by w.currency"""
        cursor.execute(SQL, (date_start,date_end, user_id,))
        return DB.namedtuplefetchall(cursor)
    
    def list_transaction_group_day(cursor, request,date_start,date_end,direction="cost",filtr_currency="",type_period=1):
        """ select transaction from DB"""
        user = request.user
        user_id=user.id
        filtr_currency = DB.GetCurrancyUser(user)    
        date_end = date_end+timedelta(days=1)
        
        if direction=="cost":
            t_sum = "0"
            t_sum2 = "-1000000000"
        else:
            t_sum = "1000000000000"
            t_sum2 = "0"
            
        if  type_period==1:
             SQLStart = """ select  DATE(t.date) as date, """
             SQLEnd = """ group by DATE(t.date) """
        elif  type_period==2:
             SQLStart = """ select  DATE(t.date, 'start of month') as date,  """
             SQLEnd = """ group by DATE(t.date, 'start of month')  """  
        elif  type_period==3:
            SQLStart = """ select  DATE(t.date, 'start of year') as date,  """
            SQLEnd = """ group by DATE(t.date, 'start of year')  """        
            
        SQL = """   w.currency,SUM(t.suma) as suma              
              from myfin_transactions as t
              left join myfin_categories as c on c.id = t.category
              left join myfin_wallets as w on w.id = t.id_wallet 
              where t.suma<%s and t.suma>%s and (t.date>=%s and t.date<%s)  and w.currency=%s  
              and w.user_id=(%s)"""
  
        SQL = SQLStart + SQL + SQLEnd                 
             
        cursor.execute(SQL, (t_sum,t_sum2,date_start,date_end, filtr_currency, user_id,))
        return DB.namedtuplefetchall(cursor) 
    
    def list_transaction_group_direction(cursor, request,date_start,date_end):
        """ select transaction from DB"""
        user = request.user
        user_id=user.id
        filtr_currency = DB.GetCurrancyUser(user)    
            
        SQL = """ select  c.direction as direction, SUM(t.suma) as suma              
              from myfin_transactions as t
              left join myfin_categories as c on c.id = t.category
              left join myfin_wallets as w on w.id = t.id_wallet 
              where (t.date>=%s and t.date<%s)  and w.currency=%s  
              and w.user_id=(%s) and (c.direction = 'Profit' or c.direction = 'Expense' )group by c.direction"""
        cursor.execute(SQL, (date_start,date_end, filtr_currency, user_id,))
        return DB.namedtuplefetchall(cursor)     
    
    # add transaction in bd
    
    
    def add_transaction(id, sum_transaction, category_id,id_exchange=None, comment = ''):
        new_t = Transactions()
        new_t.id_wallet = id
        new_t.suma = sum_transaction
        new_t.category = category_id
        new_t.id_exchange = id_exchange
        new_t.comment = comment
        new_t.date = datetime.now()
        new_t.save()
    
    def del_transaction(id):
        raw_one = Transactions.objects.filter(id=id)
        if raw_one.exists():
            id_exchange = raw_one[0].id_exchange   
            
            if id_exchange !=None:
                all_row = Transactions.objects.filter(id_exchange=id_exchange).all() 
                for w_row in all_row:
                    DB.update_ballance(w_row.id_wallet,-w_row.suma)
                    Transactions.objects.filter(id=w_row.id).delete()    
                
                Exchanges.objects.filter(id=id_exchange.id).delete()
            else:
                 DB.update_ballance(raw_one[0].id_wallet,-raw_one[0].suma)
                 Transactions.objects.filter(id=raw_one[0].id).delete()
    
    # add exchange in bd   
    
    def add_exchange(id_wallet_from, id_wallet_to, suma_from,suma_to,course):
        new_e = Exchanges()
        new_e.id_wallet_from = id_wallet_from
        new_e.id_wallet_to = id_wallet_to
        new_e.suma_from = suma_from
        new_e.suma_to = suma_to
        new_e.course = course
        new_e.date = datetime.now()
        new_e.save()
        
        category_id = DB.GetAddDopCategory(2,'exchange')
                 
        DB.add_transaction(id_wallet_from,-suma_from,category_id,new_e)
        DB.add_transaction(id_wallet_to,suma_to,category_id,new_e)
        DB.update_ballance(id_wallet_from,-suma_from)
        DB.update_ballance(id_wallet_to,suma_to)
       
    def GetAddDopCategory(dop_cat_id,name):
        raw_one = Categories.objects.filter(dop_cat_id=dop_cat_id)
        if raw_one.exists():
            return raw_one[0].id
        else:
            new_c = Categories()
            new_c.name = name
            new_c.hidden = True
            new_c.dop_cat_id = dop_cat_id
            new_c.save() 
            return new_c.id
        
    def GetCurrancyUser(user):
        currency_all = Profile.objects.filter(user=user).all();
        if currency_all.exists():
            return currency_all[0].currency
        else:
            return ''         
    
    def del_exchange(id):
        Transactions.objects.filter(id=id).delete()  
        
    #BALLANCE
    
     # add balance in bd
    def add_ballance(id, total):
        new_b = Ballance()
        new_b.id_wallet = id
        new_b.total = total
        new_b.save()
    
        # update ballance in bd
    
    
    def update_ballance(id, total):
        edit_b = Ballance.objects.get(id_wallet=id)
        edit_b.total = edit_b.total + total
        edit_b.save()
