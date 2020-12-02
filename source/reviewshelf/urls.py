"""reviewshelf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings
from .views import Index, MyAccount, MyAccountUpdate, BalanceHistoryView, AllItems, ItemCreateView, load_sub_category
from reviewapp.account import views as account_views
from reviewapp.review import views as review_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('logout/', account_views.get_logout, name='logout'),
    path('login/', account_views.UserLoginView.as_view(), name='login'),
    path('signup/', account_views.UserRegistrationView.as_view(), name='signup'),
    path('myaccount/', MyAccount.as_view(), name='my_account'),
    path('myaccount/update/<pk>', MyAccountUpdate.as_view(), name='update_account'),
    path('myaccount/item/list/', AllItems.as_view(), name='item_list'),
    path('myaccount/item/create/', ItemCreateView.as_view(), name='item_create'),
    path('myaccount/balance/history/', BalanceHistoryView.as_view(), name='balance_history'),
    path('account/', include('reviewapp.account.password.urls')),
    path('ajax/load/', load_sub_category, name='load_sub_category'),

    path('items/<slug>', review_views.ProductDetailsView.as_view(), name="product_details")
]
if settings.DEBUG:
    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns