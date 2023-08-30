from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('accounts/login/',views.LoginPage,name='a_login'),
    path('accounts/signup/',views.SignupPage,name='signup'),
    path('accounts/logout/',views.LogoutPage,name='log_out'),
    path('home/',views.home,name='home'),
    path('account/login/admin',views.admin_login,name='admin_login'),
    path('drink/group',views.Drink_group_view,name='drink_group'),
    path('drink/',views.Drink_view,name='drink'),
    path('drink/ingredient/<int:id>',views.Ingredient2_view,name='Ingredient'),
    path('buy/ingredient/',views.Ingredient_view,name='buy_ingredient'),
    path('drink/group/form',views.Drink_group_form_template,name='drink_group_form'),
    path('drink/add/ingredient/<int:id>',views.Ingredient_two_form_template,name='add_ingredient'),
    path('add/drink/form',views.add_drink_form,name='add_drink_form'),
    path('drink/buy/ingredient/form',views.Ingredient_form_template,name='drink_ingredient_form'),
    path('check/',views.Info_user_view,name='admin_check'),
    path('change/ingredient/<int:id>',views.change_ingredient2,name='change_ingredient2'),
    path('change/buy/ingredient/<int:id>',views.change_ingredient,name='change_ingredient'),
    path('change/drink/group/<int:id>',views.change_drink_group,name='change_drink_group'),
    path('change/drink/<int:id>',views.change_drink,name='change_drink'),
    path('delete/drink/<int:id>',views.delete_drink,name='delete_drink'),
    path('delete/drink/group/<int:sid>',views.delete_drink_group,name='delete_drink_group'),
    path('delete/buy/ingredient/<int:id>',views.delete_ingredient,name='delete_buy_ingredient'),
    path('delete/ingredient/<int:id>',views.delete_ingredient2,name='delete_ingredient'),
    path('caculator/ingredient/<int:id>',views.caculator,name='caculator'),
    path('change/password',views.change_password,name='change_password'),
    path('check/sms/<password>/<phone>/<code>',views.check_password_sms,name='check_sms')
]