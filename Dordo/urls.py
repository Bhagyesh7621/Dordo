"""Dordo URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from med.form import PassResetForm,SetNewPassForm
from django.contrib.auth import views as auth_views

from med.views import AboutView, Add_to_cartView, Add_to_wishlist, \
    AddressDeleteView, AllproductView, CartView, CheckoutView, \
    ContactView, DeleteView, IndexView, ListDeleteView, LoginView,\
    OrderView, ProductInfoView, ProfileView, ShopView, \
    SignupView,SigninView,LogoutView,ChangePassView, UpdateaddressView,\
    WishListView, clearcart, minus_quantity, pluse_quantity, \
    CustomerAddressView

urlpatterns = [
    path('', ShopView),
    path('admin/', admin.site.urls),
    path('index/',IndexView ),
    path('login/',LoginView),
    path('signup/',SignupView),
    path('signin/',SigninView),
    path('out/',LogoutView),
    path('shop/',ShopView),
    path('passchange/',ChangePassView),
    path('profile/',ProfileView),
    path('contact/',ContactView),
    path('about/',AboutView),
    path('productinfo/<int:id>/',ProductInfoView),
    path('cart/',CartView),
    path('addtocart/<int:id>/', Add_to_cartView),
    path('wishlist/',WishListView),
    path('addtowishlist/<int:id>/', Add_to_wishlist),
    path('pluscart/<int:id>/', pluse_quantity),
    path('minuscart/<int:id>/', minus_quantity),
    path('Delete/<int:id>/',DeleteView),
    path('clearcart/', clearcart),
    path('Listdelete/<int:id>/',ListDeleteView),
    path('address/',CustomerAddressView),
    path('Addressdelete/<int:id>/',AddressDeleteView),
    path('Addressupdate/<int:id>/',UpdateaddressView),
    path('order/', OrderView),
    path('checkout/', CheckoutView),
    path('allproducts/',AllproductView),
    
    #Passchange
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='password_reset.html',form_class=PassResetForm), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=SetNewPassForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),
  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
