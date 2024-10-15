from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import Loginform, MyPasswordChangeForm, MyPasswordResetForm, Mysetpasswordform

urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('cart/', views.show_cart, name='showcart'), 
    path('pluscart/', views.plus_cart, name='pluscart'),
   path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),

    
    
    
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    
   path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=Loginform), name='login'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    
    path('registration/', views.customerregistrationform.as_view(), name='customerregistration'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='app/password_change.html', form_class=MyPasswordChangeForm, success_url='/password_change_done/'), name='passwordchange'),
    
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    
    
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='app/passwordresset.html', form_class=MyPasswordResetForm), name='password_reset'),
    
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/passwordresetdone.html'), name='password_reset_done'),

     path('accounts/reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/passwordresetconfirm.html',
        form_class=Mysetpasswordform,
        success_url='/accounts/password_reset/complete/'
    ), name='password_reset_confirm'),

    path('accounts/password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/passwordresetcomplete.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
