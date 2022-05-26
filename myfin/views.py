from django.db import connection
from .db import DB

from django.shortcuts import  render
from django.http import HttpResponseRedirect,HttpResponse
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

from django.utils.translation import gettext,get_language
from django.contrib.auth import login, authenticate

from .forms import  UserForm,UserRegistrationForm,ProfileForm
from .forms import  NewWallet,NewTransaction,EditWallet,EditCategory,Qwestion,NewCategory,NewExchange,Reports
from django.contrib import messages

from .graph import GRAPH
import os
from django.conf import settings
import locale
import sys

   
# get wallets from bd 
def index(request):
    if request.user.is_authenticated == True:
        cursor = connection.cursor()
        if request.method == "POST":
            actions = request.POST.get("actions")
            id = int(request.POST.get("id"))
            if actions == 'wallet_delete' and id > 0:
                DB.del_wallet(cursor,id)
                return HttpResponseRedirect('/')
            elif actions == 'transaction_delete' and id > 0:

                DB.del_transaction(id)
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
     
        el_categories = DB.list_categories(cursor,request)    
        el_wallets = DB.list_wallets(cursor,request)
        
        time = datetime.now()
        timeStart = datetime(datetime.today().year, 1, 1)
        date_start = timeStart.strftime("%Y-%m-01")
        date_end = time.strftime("%Y-%m-%d")
        
        el_transaction = DB.list_transaction(cursor,request,date_start,date_end,len(el_wallets),0) 
       
        return render(request, "index.html", {"el_wallets": el_wallets,"el_categories": el_categories,"el_transaction": el_transaction,
                                              'form_add_wallet': NewWallet(),'graph_cost_category': graph_cost_category(cursor,request),
                                              'graph_cost_day': graph_cost_day(cursor,request),'graph_profit_cost': graph_profit_cost(cursor,request)})
    else:
       return render(request, "index.html") 


# wallets
def wallets(request):
     if request.user.is_authenticated == True:
         cursor = connection.cursor()
         
         if request.method == "POST":
             
             actions = request.POST.get("actions")
             id = int(request.POST.get("id"))
             
             if actions == 'wallet_add':
                name = request.POST.get("wallet_name")
                currency = request.POST.get("currency")
                total = request.POST.get("ballance")
                image = request.POST.get("image")
                DB.add_wallet(cursor,name,currency,total,image,request)
 
                return HttpResponseRedirect('/wallets')
             
             elif actions == 'wallet_delete'and id > 0:
                 DB.del_categories(cursor,id)
                 return HttpResponseRedirect('/categories')  
             
             elif actions == 'wallet_edit' and id > 0:
                 category_name = request.POST.get("category_name")
                 category_direction = request.POST.get("category_direction")
                 image = request.POST.get("image")
                 DB.edit_categories(cursor,id,category_name,category_direction,image)
                 return HttpResponseRedirect('/categories')             
    
         el_wallets = DB.list_wallets(cursor,request)
         path = os.path.join(settings.STATIC_ROOT, 'icon/wallets/')
         img_list = os.listdir(path)
         
         return render(request, "wallets.html", {"el_wallets": el_wallets,'form_add_wallet': NewWallet(),'imgs': img_list})
     else:
         return render(request, "wallets.html")

# add wallet 
def add_wallet(request):
    
    
    if request.method == "POST":
        cursor = connection.cursor()
        name = request.POST.get("wallet_name")
        currency = request.POST.get("currency")
        total = request.POST.get("ballance")
        image = request.POST.get("image")
        DB.add_wallet(cursor,name,currency,total,image,request)
        return HttpResponseRedirect('/wallets')


# edit wallet 
def edit_wallet(request):
    
    
    if request.method == "POST":
        cursor = connection.cursor()
        id = request.POST.get("id")
        name = request.POST.get("name")
        currency = request.POST.get("currency")
        image = request.POST.get("image")
        DB.edit_wallet(cursor,id,name,currency,image,request)
        return HttpResponseRedirect('/wallets')
     
    path = os.path.join(settings.STATIC_ROOT, 'icon/wallets/')
    img_list = os.listdir(path)
        
    return render(request, "edit_wallet.html", {'form_edit_wallet': EditWallet(request=request),'imgs': img_list})
 

# categories
def categories(request):
     if request.user.is_authenticated == True:
         cursor = connection.cursor()
         
         if request.method == "POST":
             
             actions = request.POST.get("actions")
             id = int(request.POST.get("id"))
             
             if actions == 'category_add':
                 name = request.POST.get("category_name")
                 direction = request.POST.get("category_direction")
                 image = request.POST.get("image")
                 DB.add_categories(cursor,name,direction,image,request)     
                 return HttpResponseRedirect('/categories')
             
             elif actions == 'category_delete'and id > 0:
                 DB.del_categories(cursor,id)
                 return HttpResponseRedirect('/categories')  
             
             elif actions == 'category_edit' and id > 0:
                 category_name = request.POST.get("category_name")
                 category_direction = request.POST.get("category_direction")
                 DB.edit_categories(cursor,id,category_name,category_direction)
                 return HttpResponseRedirect('/categories')             
    
         el_categories_profit = DB.list_categories(cursor,request,"Profit")
         el_categories_expense = DB.list_categories(cursor,request,"Expense")
         path = os.path.join(settings.STATIC_ROOT, 'icon/category/')
         img_list = os.listdir(path)
     
         return render(request, "categories.html", {"el_categories_profit": el_categories_profit,
                                                    "el_categories_expense": el_categories_expense,'form_add_category': NewCategory(),'imgs': img_list})
     else:
         return render(request, "categories.html")

# add wallet 
def add_category(request):  
    
    if request.method == "POST":
        cursor = connection.cursor()
        name = request.POST.get("name")
        direction = request.POST.get("direction")
        image = request.POST.get("image")
        DB.add_categories(cursor,name,direction,image,request)     
        return HttpResponseRedirect('/categories')
        
# edit categories
def edit_categories(request):
         if request.method == "POST":
             cursor = connection.cursor()
             id = int(request.POST.get("id"))
             name = request.POST.get("name")
             direction = request.POST.get("direction")  
             image = request.POST.get("image")
             DB.edit_categories(cursor,id,name,direction,image)
             return HttpResponseRedirect('/categories')
          
         path = os.path.join(settings.STATIC_ROOT, 'icon/category/')
         img_list = os.listdir(path)
         return render(request, "edit_categories.html", {'form_edit_category': EditCategory(request=request),'imgs': img_list})
     
       
       
# add transaction 
def add_transaction(request):
    if request.method == "POST":
        id = int(request.POST.get("wallet"))
        sum_transaction = int(request.POST.get("sum_transaction"))
        category_id = request.POST.get("category")
        direction = request.POST.get("direction")
        comment = request.POST.get("comment")
          
        if sum_transaction != 0:
           # direction_transaction = DB.direction_transaction_for_category(cursor,category_id) 
            if direction=='Expense': 
               sum_transaction = sum_transaction * -1
            
            DB.add_transaction(id,sum_transaction,category_id,None,comment)
            DB.update_ballance(id,sum_transaction)
            
            return HttpResponseRedirect('/')
        
    return render(request, "add_transaction.html",{'form_add_transaction': NewTransaction(request=request)})

# add excange 
def add_exchange(request):
    if request.method == "POST":
        wallet_from = int(request.POST.get("wallet_from"))
        wallet_to= int(request.POST.get("wallet_to"))
        sum_transaction_from = int(request.POST.get("sum_transaction_from"))
        sum_transaction_to = int(request.POST.get("sum_transaction_to"))
        
        sum_from = sum_transaction_from
        sum_to = sum_transaction_to
        course_to = sum_transaction_to/sum_transaction_from

        DB.add_exchange(wallet_from, wallet_to, sum_from,sum_to,course_to)  

            
        return HttpResponseRedirect('/')
        
    return render(request, "add_exchange.html",{'form_add_exchange': NewExchange(request=request)})
     
# transaction
def transaction(request):
    if request.user.is_authenticated == True:
        cursor = connection.cursor()
        if request.method == "POST":
             actions = request.POST.get("actions")
             id = int(request.POST.get("id"))
             if actions == 'transaction_add':
                 sum_transaction = int(request.POST.get("sum_transaction"))
                 category_id = request.POST.get("category")
                 comment = request.POST.get("comment")
                 
                 DB.add_transaction(id,sum_transaction,category_id,None,comment)
                 DB.update_ballance(id,sum_transaction)         
          
                 return HttpResponseRedirect('/transaction')
             
             elif actions == 'transaction_delete'and id > 0:
                 DB.del_transaction(id)
                 return HttpResponseRedirect('/transaction')  
      
        time = datetime.now()
        timeStart = datetime(datetime.today().year, 1, 1)
        date_start = timeStart.strftime("%Y-%m-01")
        date_end = time.strftime("%Y-%m-%d")
        
        try:
            filtr_id_wallet = int(request.POST.get("id_wallet"))
            filtr_id_category = int(request.POST.get("id_category"))
            filtr_date_start = request.POST.get("date_start")
            filtr_date_end = request.POST.get("date_end")
            filtr_currency = request.POST.get("currency")
        except:
            filtr_id_wallet = 0 
            filtr_id_category = 0
            filtr_date_start = date_start
            filtr_date_end = date_end
            filtr_currency = "0"
        
        if request.method == "GET" and  filtr_id_wallet == 0:
            try:
                filtr_id_wallet = int(request.GET.get("id_wallet"))
            except:
                filtr_id_wallet = 0

        if request.method == "GET" and  filtr_id_category == 0:
            try:
                filtr_id_category = int(request.GET.get("id_category"))
            except:
                filtr_id_category = 0                
           
        el_transaction = DB.list_transaction(cursor,request,filtr_date_start,filtr_date_end,500,filtr_id_wallet,filtr_id_category,filtr_currency) 
        el_wallets = DB.list_wallets(cursor,request)
        el_categories = DB.list_categories(cursor,request)
    
        return render(request, "transaction.html", {"el_transaction": el_transaction,"el_wallets": el_wallets
                                                    ,"el_categories": el_categories,"date_start": filtr_date_start
                                                    ,"date_end": filtr_date_end,"filtr_id_wallet": filtr_id_wallet
                                                    ,"filtr_id_category": filtr_id_category ,"filtr_currency": filtr_currency})     
    else:
        return render(request, "transaction.html")
    
def reports(request):
    cursor = connection.cursor()
    try:
        report_id = int(request.GET.get("id"))
    except:
        report_id = 1 
  
    time = datetime.now()
    date_start =  datetime.now().date() - timedelta(days=30)
    date_end = time 


    date_start = date_start.strftime("%Y-%m-01")    
    date_end = date_end.strftime("%Y-%m-%d") 
    
    
    filtr_date_start = request.GET.get("date_start")
    filtr_date_end = request.GET.get("date_end")
    
    filtr_period_month= request.GET.get("period_month")
    if filtr_period_month ==None:
        filtr_period_month = 1
    
    currency = request.GET.get("currency")
    
    if currency ==None:
        currency = "UAH"
    
    if filtr_date_start ==None:
        filtr_date_start = date_start
        
    if filtr_date_end ==None:
        filtr_date_end = date_end
    
    if report_id == 1:
        date_return = report_graph_category(cursor,request,filtr_date_start,filtr_date_end,'cost','category',currency)
    elif report_id == 5:
        date_return = report_graph_category(cursor,request,filtr_date_start,filtr_date_end,'profit','category',currency) 
    elif report_id == 2:
        filtr_date_start_g = datetime.now().date() - timedelta(days=6)
        filtr_date_end_g = time
        date_return = report_graph_day(cursor,request,filtr_date_start_g,filtr_date_end_g,'profit',currency)  
    elif report_id == 3:
        if filtr_period_month=='1':
            filtr_date_start_g = datetime.now().date() + relativedelta(months=-5)
            filtr_date_end_g = time.date()
        elif filtr_period_month=='2':    
            filtr_date_start_g = datetime.now().date().replace(month=1, day=1) 
            filtr_date_end_g = time.date()
        elif filtr_period_month=='3':    
            filtr_date_start_g = datetime.now().date().replace(month=1, day=1) + relativedelta(years=-1)
            filtr_date_end_g = datetime.now().date().replace(month=12, day=31)+ relativedelta(years=-1)
        else:

            filtr_date_start_g = datetime.strptime(filtr_period_month+"-01-01","%Y-%m-%d").date()   
            filtr_date_end_g = datetime.strptime(filtr_period_month+"-12-31","%Y-%m-%d").date() 
            
        date_return = report_graph_day(cursor,request,filtr_date_start_g,filtr_date_end_g,'profit',currency,2)  
    elif report_id == 4:
        filtr_date_start_g = datetime.now().date() + relativedelta(years=-6)
        filtr_date_end_g = time
        date_return = report_graph_day(cursor,request,filtr_date_start_g,filtr_date_end_g,'profit',currency,3)  
        
    return render(request, "reports.html",{"report_id": report_id,"report_graph":date_return.get("image_graph")                                           
                                           ,"data_svod":date_return.get("data_svod"),'filtr_currency':date_return.get("currency")
                                           ,"date_start": filtr_date_start,"date_end": filtr_date_end
                                           ,'form_report': Reports(request=request)})    


def signup(request):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect('/')
    return render(request, 'signup.html', {'form': form})

 
def qwestion(request):  
    if request.method == "POST":
        try:
            form_qwestion = int(request.POST.get("form_qwestion"))       
        except:
            form_qwestion = 0
        
        try:
            sum_transaction = int(request.POST.get("sum_transaction"))
            id_wallet = int(request.POST.get("id_wallet"))
        except:
            sum_transaction = 0
            id_wallet = 0
                
        
        if form_qwestion == 1:
            actions = request.POST.get("actions")
            id = int(request.POST.get("id"))
            text_qwestion = gettext(request.POST.get("text_qwestion"))
            
            if actions == 'category_delete':
                url_post = '/categories/'
            else:
                url_post = '/'
                
            form_data =  {"actions": actions,
                          "id": id,
                          "sum_transaction": sum_transaction,
                          "id_wallet": id_wallet,
                          "text_qwestion": text_qwestion,
                          "url_post": url_post}
    
            return render(request, "qwestion.html", {"form_data": form_data})
        
        else: 
            cursor = connection.cursor()
            actions = request.POST.get("actions")
            id = int(request.POST.get("id"))
               
            if actions == 'wallet_delete' and id > 0:
                DB.del_wallet(cursor,id)
                return HttpResponseRedirect('/')
            
            elif actions == 'transaction_delete' and id > 0:

                DB.del_transaction(id)
                return HttpResponseRedirect('/')
            
            elif actions == 'category_delete'and id > 0:
                DB.del_categories(cursor,id)
                return HttpResponseRedirect('/categories')  
            
            elif actions == 'qwestion':
                DB.del_transaction(id)
                return HttpResponseRedirect('/')
                    
           
    return render(request, "qwestion.html", {'form_qwestion': Qwestion(request=request)})

def userpage(request):
	return render(request , "user.html")

def edit_profil(request):
    if request.method == 'POST':
       user_form = UserForm(request.POST, instance=request.user)
       profile_form = ProfileForm(request.POST, instance=request.user.profile)
       if user_form.is_valid() and profile_form.is_valid():
           user_form.save()
           profile_form.save()
           messages.success(request, gettext('profil_update_sucess'))
           return HttpResponseRedirect('/user')
       else:
           messages.error(request, gettext('profil_update_no_sucess'))
    else:
       user_form = UserForm(instance=request.user)
       profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profil.html', {
       'user_form': user_form,
       'profile_form': profile_form
   })

def about(request):   
    return render(request, "about.html")

   
def get_currance_wallet(request):
    id_wallet = int(request.GET.get("id_wallet"))
    currancy_wallet = DB.get_wallet_currancy(id_wallet)
    return HttpResponse(currancy_wallet)

def graph_cost_category(cursor,request):
    time = datetime.now()
    date_start =  datetime.now().date() - timedelta(days=30)
    date_end = time     
    
    date_start = date_start.strftime("%Y-%m-01")    
    date_end = date_end.strftime("%Y-%m-%d") 
    
    
    el_transaction = DB.list_transaction_group_category(cursor,request,date_start,date_end)     
    
    data_names = []
    data_values=[]
    number = 0
    for el in el_transaction:
        if el.category!='ballance' and el.category!='exchange':
            data_names.append('' + el.category + ': ' + str(-el.suma))
            data_values.append(-el.suma)
            number+=1
            if number==5:
                break       
     
    data_names = list(data_names)
    data_values = list(data_values)        

    return GRAPH.graph_pie_with_center(data_names,data_values,True)
    
def graph_cost_day(cursor,request):
    time = datetime.now()
    date_start =  datetime.now().date() - timedelta(days=6)
    date_end = time
    
    data_names = []
    data_values=[]
    
    days = [date_start + timedelta(days=x) for x in range((date_end.date()-date_start).days + 1)]

    for day_l in days:
        data_names.append(day_l.strftime('%d'))
        data_values.append(0)
        
        
    el_transaction = DB.list_transaction_group_day(cursor,request,date_start,date_end)     
    

    for el in el_transaction:
        locdate = el.date
        date_start = locdate
        
        res_date = date_start[8:10];
        ind_res_date = data_names.index(res_date)
        if ind_res_date<0:
            data_names.append()
            data_values.append(-el.suma)
        else:    
           data_values[ind_res_date] = -el.suma
     
    data_names = list(data_names)
    data_values = list(data_values)
    
    if len(data_names) != 0:        
        return GRAPH.graph_bar(data_names,data_values)    
    
def graph_profit_cost(cursor,request):
    time = datetime.now()
    date_start =  datetime.now().date() - timedelta(days=6)
    date_end = time
    
    data_names = []
    data_values=[]
        
    el_transaction = DB.list_transaction_group_direction(cursor,request,date_start,date_end)     
    
    sum =0
    for el in el_transaction:
            sum = sum + el.suma
            sum_g = el.suma
            if sum_g < 0 :
                sum_g = -sum_g
            if (el.direction=='Profit'):
                text_legend = gettext('profit')
            else:
                text_legend = gettext('cost')
            data_names.append('' + text_legend + ': ' + str(sum_g))
            data_values.append(sum_g)
            

     
    data_names = list(data_names)
    data_values = list(data_values)
    
    if len(data_names) != 0:        
        return GRAPH.graph_pie_with_center(data_names,data_values)      
 
def report_graph_category(cursor,request,date_start,date_end,direction,path_image='',filtr_currency=''):

            
        el_transaction = DB.list_transaction_group_category(cursor,request,date_start,date_end,direction,filtr_currency)     
        
        data_svod = []        
        data_names = []
        data_values=[]
        data_colors =['teal', 'brown','yellow', 'red', 'green', 'olive', 'grey','orange','silver','white','purple','blue','lime','fuchsia','aqua','maroon','navy']
        
        total = 0  
        numColor = 0
        currency = "UAH"
        for el in el_transaction:
            if el.category!='ballance' and el.category!='exchange':
                if el.suma<0:
                    sumrow = -el.suma

                else:
                    sumrow = el.suma
                    
                data_names.append('' + el.category + ': ' + str(sumrow))
                data_values.append(sumrow)
                total = total + el.suma 
                data_svod.append({'name': el.category, 'image': path_image+"/"+el.image, 'suma': sumrow, 'currency': el.currency,'color': data_colors[numColor]})
                currency = el.currency
                numColor+=1                
    
        
        data_names = list(data_names)
        data_values = list(data_values)  
        if direction=="cost":
            text_center =  gettext('total_cost') + ":" + str(total) + " " + gettext(currency)
        else:
            text_center =  gettext('total_profit') + ":" + str(total) + " " + gettext(currency)

        image_graph = GRAPH.graph_pie(data_names,data_values,data_colors,text_center,False)

        date_return = {'data_names': data_names, 'data_svod': data_svod, 'image_graph': image_graph, 'total': -total, 'currency': currency}
        
        return date_return
    
def report_graph_day(cursor,request,date_start,date_end,direction,filtr_currency='',type_period = 1):
    
    #data_report = report_graph_date(cursor,request,date_start,date_end,direction,filtr_currency,type_period)
    data_report = report_graph_date(cursor,request,date_start,date_end,"cost",filtr_currency,type_period)
    data_report2 = report_graph_date(cursor,request,date_start,date_end,"profit",filtr_currency,type_period)
  
    data_names = data_report.get("data_names")
    data_values = data_report.get("data_values")
    data_svod = data_report.get("data_svod")
    title = data_report.get("title")
    currency = data_report.get("currency")
    
    data_values2 = data_report2.get("data_values")
    #data_svod2= data_report2.get("data_svod")
    
    image_graph = ''
    if len(data_names) != 0:        
       # image_graph = GRAPH.graph_bar(data_names,data_values,False,title) 
       image_graph = GRAPH.graph_bar_double(data_names,data_values,data_values2,title) 

    date_return = {'data_names': data_names, 'data_svod': data_svod, 'image_graph': image_graph, 'currency': currency}
    
    return date_return     

def report_graph_date(cursor,request,date_start,date_end,direction,filtr_currency='',type_period = 1):
    
    data_names = []
    data_values=[]
    data_svod = [] 
    data_colors =['teal', 'brown','yellow', 'red', 'green', 'olive', 'grey','orange','silver','white','purple','blue','lime','fuchsia','aqua','maroon','navy']
    
    
    if get_language()=='uk':
        if sys.platform == 'win32':
            locale.setlocale(locale.LC_ALL, 'ukr_ukr')
        else:
            locale.setlocale(locale.LC_ALL, 'uk_UK.UTF-8')
    else:
        if sys.platform == 'win32':
            locale.setlocale(locale.LC_ALL, 'en')
        else:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')        
        
        

    if type_period==1:
        days = [date_start + timedelta(days=x) for x in range((date_end.date()-date_start).days + 1)]
        for day_l in days:
            data_names.append(day_l.strftime('%d'))
            data_values.append(0)
        if direction=='cost':    
            title = gettext('cost_day_graph') 
        else:
            title = gettext('profit_day_graph') 
    elif type_period==2:
        date_1 = date_start
        while date_1<=date_end:
            data_names.append(date_1.strftime('%b %y'))
            data_values.append(0)
            date_1 = date_1 + relativedelta(months=1)
            
        """month = [date_start + relativedelta(months=-x) for x in range((date_end-date_start).days/30 + 1)]
        for month_l in month:
            data_names.append(month_l.strftime('%m'))
            data_values.append(0)"""
            
        if direction=='cost':    
            title = gettext('cost_month_graph') 
        else:
            title = gettext('profit_month_graph') 

    elif type_period==3:  
        if direction=='cost':    
            title = gettext('cost_year_graph') 
        else:
            title = gettext('profit_year_graph') 

        
    el_transaction = DB.list_transaction_group_day(cursor,request,date_start,date_end,direction,filtr_currency,type_period)     
  
    numColor = 0
    currency = "UAH"

    for el in el_transaction:
        locdate = el.date
        date_start = locdate
        
        if type_period==1:
            res_date = date_start[8:10];
            ind_res_date = data_names.index(res_date)
        elif type_period==2:
            date_m = datetime.strptime(el.date, "%Y-%m-%d").date()
            ind_res_date = data_names.index(date_m.strftime('%b %y'))    
              
        
        if el.suma<0:
            sumrow = -el.suma

        else:
            sumrow = el.suma
        
        if type_period==1:   
            if ind_res_date<0:
                data_names.append()
                data_values.append(sumrow)
            else:    
               data_values[ind_res_date] = sumrow
              
        elif type_period==2: 
            if ind_res_date<0:
                data_names.append(date_m.strftime('%Y-%m'))
                data_values.append(sumrow)
            else:    
               data_values[ind_res_date] = sumrow
               
        elif type_period==3: 
            date_m = datetime.strptime(el.date, "%Y-%m-%d").date()
            ind_res_date = el.date
            data_names.append(date_m.strftime('%Y'))
            data_values.append(sumrow)  
            
           
        data_svod.append({'date': ind_res_date,  'suma': sumrow, 'currency': el.currency,'color': data_colors[numColor]})
     
    data_names = list(data_names)
    data_values = list(data_values)

    date_return = {'data_names': data_names,'data_values': data_values, 'data_svod': data_svod, 'currency': currency, 'title': title}
    
    return date_return   
    