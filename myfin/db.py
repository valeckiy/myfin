
from collections import namedtuple
from .models import Wallets,Ballance,Transactions,Categories
from datetime import datetime,timedelta

class DB:
    

    def namedtuplefetchall(cursor):
        "Return all rows from a cursor as a namedtuple"
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]

    #WALLETS
    
    
    def list_wallets(cursor):
        SQL = """ select  w.name,b.total, w.currency, w.id from myfin_wallets as w 
               left join myfin_ballance as b on b.id_wallet=w.id order by name """
        cursor.execute(SQL)
        return DB.namedtuplefetchall(cursor)
    
    
    def add_wallet(cursor, name, currency, ballance):
        new_w = Wallets()
        new_w.name = name
        new_w.currency = currency
        new_w.save()
    
        max_id = Wallets.objects.all().last().id
        total = ballance
        DB.add_transaction(max_id, total, 0)
        DB.add_ballance(max_id, total)
    
        return {"name": new_w.name, "currency": new_w.currency, "total": total}
    
    
    def del_wallet(cursor, id):
        Wallets.objects.filter(id=id).delete()
        Ballance.objects.filter(id_wallet=id).delete()
        Transactions.objects.filter(id_wallet=id).delete()
    
    #CATEGORIES
    
    
    def list_categories(cursor):
        return Categories.objects.all().order_by("direction","name")
    
    
    def add_categories(cursor, name, direction):
        new_c = Categories()
        new_c.name = name
        new_c.direction = direction
        new_c.save()
    
    
    def edit_categories(cursor, id, name, direction):
        edit_c = Categories.objects.get(pk=id)
        edit_c.name = name
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
    
    def list_transaction(cursor, date_start,date_end,limit=100, filtr_id_wallet=0,filtr_id_category=0):
        """ select transaction from DB"""
        date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
        date_end = datetime.strptime(date_end, "%Y-%m-%d").date()+timedelta(days=1)
        SQL = """ select  t.date, w.name as wallet, c.name as category, t.suma,
              w.currency,t.id,w.id as id_wallet
              from myfin_transactions as t
              left join myfin_categories as c on c.id = t.category
              left join myfin_wallets as w on w.id = t.id_wallet 
              where (t.date>=%s and t.date<%s) and(w.id=%s or %s=0)and(t.category=%s or %s=0)
              order by t.date DESC limit %s """
        cursor.execute(SQL, (date_start,date_end,filtr_id_wallet, filtr_id_wallet
                             , filtr_id_category,filtr_id_category,limit,))
        return DB.namedtuplefetchall(cursor)
    
    # add transaction in bd
    
    
    def add_transaction(id, sum_transaction, category_id):
        new_t = Transactions()
        new_t.id_wallet = id
        new_t.suma = sum_transaction
        new_t.category = category_id
        new_t.date = datetime.now()
        new_t.save()
    
    def del_trancaction(id):
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
