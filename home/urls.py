from django.urls import path,include,re_path
from myfin import views
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

 
urlpatterns = i18n_patterns(
    path('', views.index, name='index'),
    re_path('add_wallet/$', views.add_wallet, name='add_wallet'),
    path('wallets/', views.wallets, name='wallets'),
    re_path('edit_wallet/$', views.edit_wallet, name='edit_wallet'),
    path('categories/', views.categories, name='categories'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_categories/', views.edit_categories, name='edit_categories'),
    re_path('transaction/$', views.transaction, name='transaction'),
    re_path('add_transaction/$', views.add_transaction, name='add_transaction'),
    re_path('reports/$', views.reports, name='reports'),
    path('add_exchange/', views.add_exchange, name='add_exchange'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('qwestion/', views.qwestion, name='qwestion'),
    path('about/', views.about, name='about'),
    path("user/", views.userpage, name = "userpage"),
    path("edit_profil/", views.edit_profil, name = "edit_profil"),
    
    path("get_currance_wallet/", views.get_currance_wallet, name = "get_currance_wallet"),
)
