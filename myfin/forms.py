from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm 
from django.utils.translation import  gettext_lazy
from datetime import datetime,timedelta
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from .models import Categories,Wallets, Profile



class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(gettext_lazy('email_exist'))
        return email
    
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name','last_name')

        
class ProfileForm(forms.ModelForm):
    currency_main = {
      'UAH': 'UAH',
      'USD': 'USD',
      'EUR': 'EUR'
    }

    currency_choise = list(currency_main.items())
    currency = forms.ChoiceField(label=gettext_lazy('currency'), choices=currency_choise, required=True)
    
    class Meta:
        model = Profile
        fields = ('currency', )        
        
        
class NewWallet(forms.Form):       
     wallet_name = forms.CharField(label=gettext_lazy('name'),initial=gettext_lazy('wallet'))
     
     currency_main = {
       'UAH': 'UAH',
       'USD': 'USD',
       'EUR': 'EUR'
     }

     currency_choise = list(currency_main.items())
     currency = forms.ChoiceField(label=gettext_lazy('currency'), choices=currency_choise, required=True)
      
     ballance = forms.IntegerField(label=gettext_lazy('balance'))
     image = forms.CharField(label=gettext_lazy('image'),widget=forms.HiddenInput)
     
     helper = FormHelper()
     helper.form_class = 'form-horizontal'
     helper.layout = Layout(
         Field('wallet_name'),
         Field('currency'),
         Field('ballance'),

    )
     
class EditWallet(forms.Form):     
     id = forms.IntegerField(widget=forms.HiddenInput)
     name = forms.CharField(label=gettext_lazy('name'))
     
     currency_main = {
       'UAH': 'UAH',
       'USD': 'USD',
       'EUR': 'EUR'
     }

     currency_choise = list(currency_main.items())
     currency = forms.ChoiceField(label=gettext_lazy('currency'), choices=currency_choise, required=True)
     image = forms.CharField(label=gettext_lazy('image'),widget=forms.HiddenInput)
     
     def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)    
        
        g_id = request.GET.get("id")
        g_name = request.GET.get("name")
        g_currency = request.GET.get("currency")
        g_image = request.GET.get("image_l")
        super(EditWallet, self).__init__(*args, **kwargs)

        self.fields['name'].initial =g_name
        self.fields['currency'].initial =g_currency
        self.fields['id'].initial =g_id
        self.fields['image'].initial =g_image
        
     helper = FormHelper()
     helper.form_class = 'form-horizontal'
     helper.layout = Layout(
         Field('name'),
         Field('currency'),
    )    
  
class NewCategory(forms.Form):       
    name = forms.CharField(label=gettext_lazy('name'),initial=gettext_lazy('category'))
    
    direction_main = {
       'Profit': gettext_lazy('profit'),
       'Expense': gettext_lazy('cost')
    }
    
    direction_choise = list(direction_main.items())
    direction = forms.ChoiceField(label=gettext_lazy('direction'), choices=direction_choise, required=True)
    
    image = forms.CharField(label=gettext_lazy('image'),widget=forms.HiddenInput)
    
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
      Field('name'),
      Field('direction'),
      Field('image'),
)
     
class EditCategory(forms.Form):     
      id = forms.IntegerField(widget=forms.HiddenInput)
      name = forms.CharField(label=gettext_lazy('name'))
      
      direction_main = {
         'Profit': gettext_lazy('profit'),
         'Expense': gettext_lazy('cost')
      }

      direction_choise = list(direction_main.items())
      direction = forms.ChoiceField(label=gettext_lazy('direction'), choices=direction_choise, required=True)
      image = forms.CharField(label=gettext_lazy('image'),widget=forms.HiddenInput)
      def __init__(self, *args, **kwargs):
         request = kwargs.pop('request', None)    
         
         g_id = request.GET.get("id")
         g_name = request.GET.get("name")
         g_direction = request.GET.get("direction")
         g_image = request.GET.get("image_l")
         
         super(EditCategory, self).__init__(*args, **kwargs)

         self.fields['name'].initial =g_name
         self.fields['direction'].initial =g_direction
         self.fields['id'].initial =g_id
         self.fields['image'].initial =g_image
         
      helper = FormHelper()
      helper.form_class = 'form-horizontal'
      helper.layout = Layout(
          Field('name'),
          Field('direction'),
          Field('image'),          
     )     

class NewTransaction(forms.Form):   
     direction = forms.CharField(widget=forms.HiddenInput)
     direction_text = forms.CharField(widget=forms.HiddenInput)
     
     wallet = forms.ChoiceField(label=gettext_lazy('wallet'), required=True)
     category = forms.ChoiceField(label=gettext_lazy('category'), required=True)
     sum_transaction = forms.IntegerField(label=gettext_lazy('sum'),widget=forms.NumberInput(attrs={'autofocus': ''}))
     comment =forms.CharField(label=gettext_lazy('comment'), required=False,widget=forms.Textarea(attrs={'rows':2, 'cols':20}))
     def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)    
        user_id = request.user.id
        
        id = request.GET.get("id")
        g_direction = request.GET.get("direction")
        
        super(NewTransaction, self).__init__(*args, **kwargs)

        category_list = Categories.objects.all().filter(user=user_id,direction=g_direction).order_by("direction","name")
     
        self.fields['category'].choices = (
            (el.id,el.name)
            for el in category_list
        )
        
        wallet_list = Wallets.objects.all().filter(user=user_id).order_by("name")
     
        self.fields['wallet'].choices = (
            (el.id,el.name)
            for el in wallet_list
        )
        self.fields['wallet'].initial = id
        
        self.fields['direction'].initial = g_direction
        self.fields['direction_text'].initial = 'add_new_' + g_direction
     
     helper = FormHelper()
     helper.form_class = 'form-horizontal'
     helper.layout = Layout(
         Field('wallet'),
         Field('category'),         
         Field('sum_transaction'),
         Field('comment'),

    )    
     
     
class NewExchange(forms.Form):   
     wallet_from = forms.ChoiceField(label=gettext_lazy('wallet_from'), required=True, widget=forms.Select(attrs={"onChange":'ChangeWalletFrom()'}))
     wallet_to = forms.ChoiceField(label=gettext_lazy('wallet_to'), required=True, widget=forms.Select(attrs={"onChange":'ChangeWalletTo()'}))
     sum_transaction_from = forms.IntegerField(label=gettext_lazy('sum_from'), widget=forms.NumberInput(attrs={"onChange":'ChangeSumFrom()'}))   
     currency_from = forms.CharField(label='',disabled=True)
     sum_transaction_to = forms.IntegerField(label=gettext_lazy('sum_to'), widget=forms.NumberInput(attrs={"onChange":'ChangeSumTo()',"onfocus":'ShowHiddenFields()','autofocus': ''}))     
     currency_to = forms.CharField(label='',disabled=True)

     course = forms.DecimalField(label=gettext_lazy('course'),max_digits= 12, decimal_places= 4,initial=1.0000,disabled=True)
     
     def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)    
        user_id = request.user.id
        id = request.GET.get("id")
        
        super(NewExchange, self).__init__(*args, **kwargs)
        
        wallet_list = Wallets.objects.all().filter(user=user_id).order_by("name")
     
        self.fields['wallet_from'].choices = (
            (el.id,el.name)
            for el in wallet_list
        )
        self.fields['wallet_from'].initial = id
        
        self.fields['wallet_to'].choices = (
            (el.id,el.name)
            for el in wallet_list
        )
         
        for el in wallet_list:
            if int(id)==el.id:
               self.fields['currency_from'].initial = el.currency
       
        self.fields['currency_to'].initial = wallet_list[0].currency 
 
        
     helper = FormHelper()
     helper.form_class = 'form-horizontal'
     helper.layout = Layout(
         Field('wallet_from'),
         Field('wallet_to'), 
         Field('sum_transaction_from'),
         Field('currency_from'),
         Field('sum_transaction_to'),
         Field('currency_to'),
         Field('course'),
    )      
     
class Qwestion(forms.Form):    
                        
      id = forms.IntegerField(widget=forms.HiddenInput)
      id_wallet = forms.IntegerField(widget=forms.HiddenInput)
      sum_transaction = forms.IntegerField(widget=forms.HiddenInput)
      actions = forms.CharField(widget=forms.HiddenInput)
      text_qwestion = forms.CharField(widget=forms.HiddenInput)
      url_post = forms.CharField(widget=forms.HiddenInput)
      
      def __init__(self, *args, **kwargs):
         request = kwargs.pop('request', None)    
         
         g_id = request.GET.get("id")
         g_id_wallet = request.GET.get("id_wallet")
         g_sum_transaction = request.GET.get("sum_transaction")
         g_actions = request.GET.get("actions")
         g_text_qwestion = request.GET.get("text_qwestion")
         g_url_post = request.GET.get("url_post")
         
         super(Qwestion, self).__init__(*args, **kwargs)

         self.fields['id'].initial =g_id
         self.fields['id_wallet'].initial =g_id_wallet
         self.fields['sum_transaction'].initial =g_sum_transaction
         self.fields['actions'].initial =g_actions
         self.fields['text_qwestion'].initial = gettext_lazy(g_text_qwestion)
         self.fields['url_post'].initial = g_url_post
         
      helper = FormHelper()
      helper.form_class = 'form-horizontal'
      helper.layout = Layout(
          Field('name'),
          Field('direction'),
     )        
        
class Reports(forms.Form):   
     
     report_main = {
       '1': gettext_lazy("cost_category"),
       '5': gettext_lazy("profit_category"),
       
       '2': gettext_lazy("cost_profit_day"),
       '3': gettext_lazy("cost_profit_month"),
       '4': gettext_lazy("cost_profit_year"),

       '6': gettext_lazy("profit_cost"),
       '7': gettext_lazy("balance"),
     }
     
     report_choise = list(report_main.items())
     id = forms.ChoiceField(label='', choices=report_choise, required=True, widget=forms.Select(attrs={"onChange":'ChangeTypeReport()','class': 'special-input'}))
    
     date_start = forms.DateField(label=gettext_lazy('date_start'), required=True, 
                                  widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control',  'placeholder': 'Select a date', 'type': 'date'}))
     
     date_end = forms.DateField(label=gettext_lazy('date_end'), required=True, 
                                  widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control',  'placeholder': 'Select a date', 'type': 'date'}))
     
    
     period_month_main = {
      '1':  gettext_lazy("period_last_six_month"),
      '2':  gettext_lazy("period_this_years"),
      '3':  gettext_lazy("period_last_years"),
     }
    
     years = [datetime.now()- relativedelta(years=x) for x in range(2,5)]
     for years_l in years:
         year_f = years_l.strftime('%Y')
         period_month_main.update({year_f:year_f})

        
     three_yrs_ago = datetime.now() - relativedelta(years=3)
    

     period_month_choise = list(period_month_main.items())
     period_month = forms.ChoiceField(label=gettext_lazy('period'), choices=period_month_choise)
    
     currency_main = {
       'UAH': 'UAH',
       'USD': 'USD',
       'EUR': 'EUR'
     }

     currency_choise = list(currency_main.items())
     currency = forms.ChoiceField(label=gettext_lazy('currency'), choices=currency_choise, required=True)
     
     def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)    
        
        time = datetime.now()
        d_start =  datetime.now().date() - timedelta(days=30)
        d_end = time 
        d_start = d_start.strftime("%Y-%m-01")    
        d_end = d_end.strftime("%Y-%m-%d") 
        
        g_id = request.GET.get("id")
        g_date_start = request.GET.get("date_start")
        if g_date_start ==None:
            g_date_start = d_start
        g_date_end= request.GET.get("date_end")
        if g_date_end ==None:
            g_date_end = d_end
        
        g_period_month= request.GET.get("period_month")
        if g_period_month ==None:
            g_period_month = 1
                        

        g_currency = request.GET.get("currency")
        super(Reports, self).__init__(*args, **kwargs)
    
        self.fields['id'].initial =g_id
        self.fields['date_start'].initial =g_date_start
        self.fields['date_end'].initial =g_date_end
        self.fields['period_month'].initial =g_period_month
        self.fields['currency'].initial =g_currency
 
        
     helper = FormHelper()
     helper.form_class = 'form-horizontal'
  