from django.urls import path, reverse_lazy

from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from django.contrib.auth import views as auth_views

from . import views

from .forms import MyPasswordChangeForm

urlpatterns = [
    path('', views.menu, name="menu"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('about/', views.about, name="about"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user-page"),
    path('account/', views.account, name="account"),
    path('search/', views.search, name="search"),

    path('update_item/', views.updateItem, name="updateitem"),
    path('process_order/', views.processOrder, name="process_order"),
    path('admin/', views.dashboard, name="dashboard"),
    path('admin/items', views.items, name="items"),
    path('customer/<str:pk>', views.customer, name="customer"),
    path('orders/', views.orders, name="orders"),
    # path('order_type/<str:pk>/', views.orderType, name="order_type"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('addItem/', views.addItem, name="addItem"),
    path('update_item/<str:pk>/', views.updateitem, name="update_item"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='stores/password_reset.html'),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='stores/password_reset_sent.html'),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='stores/password_reset_form.html'),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='stores/password_reset_done.html'),
         name="password_reset_complete"),

    path('change_password/', PasswordChangeView.as_view(
        template_name='stores/change_password.html',
        success_url=reverse_lazy('password_change_done'),
        form_class=MyPasswordChangeForm
    ), name='password_change'),

    path('change_password/done/', PasswordChangeDoneView.as_view(
        template_name='stores/password_change_done.html'
    ), name='password_change_done'),

]
