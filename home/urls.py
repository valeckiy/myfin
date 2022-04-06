from django.urls import path
from myfin import views
from django.contrib import admin
 
urlpatterns = [
    path('', views.index, name='index'),
    path('add_wallet/', views.add_wallet, name='add_wallet'),
    path('add_wallet_results/', views.add_wallet_results, name='add_wallet_results'),
    path('categories/', views.categories, name='categories'),
    path('edit_categories/', views.edit_categories, name='edit_categories'),
    path('transaction/', views.transaction, name='transaction'),
    path('admin/', admin.site.urls),
]
