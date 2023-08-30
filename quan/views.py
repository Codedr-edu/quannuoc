from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Drink_group, Drink,Ingredient,Ingredient2,Info_user
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.apps import AppConfig
import random
#import twilio
import os
from twilio.rest import Client

# Create your views here.

account_sid = 'AC6781bef8617848874201927f6e233c64'
auth_token = 'c9918f43b4022f016b11fdd38086dc6d'
client = Client(account_sid, auth_token)
twilio_phone = '+15734923650'


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

@login_required(login_url='a_login')
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())
'''
@method_decorator(login_required, name='dispatch')
class Drink_group_view(generic.ListView):
    model = Drink_group
    template_name = 'drink_group.html'

    def get_queryset(self):
        add = Drink_group.objects.all()
        return add

class DetailView2(generic.DetailView):
    model = Drink_group

@method_decorator(login_required, name='dispatch')
class Drink_view(generic.ListView):
    model = Drink
    template_name = 'drink.html'

    def get_queryset(self):
        add = Drink.objects.all()
        return add

class DetailView3(generic.DetailView):
    model = Drink

@method_decorator(login_required, name='dispatch')
class Ingredient_view(generic.ListView):
    model = Ingredient
    template_name = 'buy_ingredient.html'

    def get_queryset(self):
        add = Ingredient.objects.all()
        return add[::-1]

class DetailView4(generic.DetailView):
    model = Ingredient
'''
@login_required(login_url='a_login')
def Ingredient_view(request):
    ing = Ingredient.objects.filter(user_id=request.user.id).all()
    context = {'object_list':ing}
    return render(request, 'buy_ingredient.html', context)

@login_required(login_url='a_login')
def Drink_view(request):
    ing = Drink.objects.filter(user_id=request.user.id).all()
    context = {'object_list':ing}
    return render(request, 'drink.html', context)

@login_required(login_url='a_login')
def Drink_group_view(request):
    ing = Drink_group.objects.filter(user_id=request.user.id).all()
    context = {'object_list':ing}
    return render(request, 'drink_group.html', context)

'''
@login_required(login_url='login')
def Ingredient2_view(request,id):
    model = Ingredient2.objects.filter(main_drink_id=id).first()
    return render(request,'ingredient.html',{'posts':model})


'''
'''
@method_decorator(login_required, name='dispatch')
class Ingredient2_view(generic.ListView):
    model = Ingredient2
    template_name = 'ingredient.html'

    def get_queryset(self):
        queryset = Ingredient2.objects.all()

        if self.request.GET.get('id'):
            queryset = queryset.filter(main_drink_id=self.request.GET.get('id'))
        return queryset


class DetailView4(generic.DetailView):
    model = Ingredient2
'''
@login_required(login_url='a_login')
def Ingredient2_view(request,id):
    ing = Ingredient2.objects.filter(main_drink_id=id).all()
    context = {'object_list':ing}
    return render(request, 'ingredient.html', context)


'''
s = 0
for item in ing:
s += int(item.price)
'''

def Info_user_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        model = User.objects.all()
        context = {'object_list':model[::-1]}
    return render(request, 'admin.html', context)

'''
def home(request):
    model = Course.objects.all()
    context = {'model':model}
    return render('home.html', context)
'''

@login_required(login_url='a_login')
def Drink_group_form_template(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name')
            if not Drink_group.objects.filter(name=name,user_id=request.user.id):
                dg = Drink_group(name=name,user_id=request.user.id)
                dg.save()
                dg = Drink_group.objects.filter(name=name).first()
                return redirect('drink_group')
            else:
                return redirect('drink_group_form')
    return render(request, 'drink_group_form.html')


@login_required(login_url='login')
def add_drink_form(request):
    if request.user.is_authenticated:
        dk = Drink_group.objects.filter(user_id=request.user.id).all()
        if request.method == 'POST':
            price = request.POST.get('price')
            name = request.POST.get('name')
            group_id = request.POST.get('group_name')

            drk = Drink_group.objects.filter(id=group_id,user_id=request.user.id).first()

            if drk:
                d = Drink(name=name,price=price,group=drk.name,group_id=drk.id,user_id=request.user.id,total_ingredient=0,money=0)
                d.save()
                return redirect('drink')
    return render(request, 'add_drink_form.html',{'drk':dk})

@login_required(login_url='a_login')
def Ingredient_form_template(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            price = request.POST.get('price')
            name = request.POST.get('name')
            buy_unit = request.POST.get('buy_unit')
            change_unit = request.POST.get('change_unit')
            change_value = request.POST.get('change_value')
            brand = request.POST.get('brand')

            new_ing = Ingredient(name=name,price=price,buy_unit=buy_unit,change_value=change_value,change_unit=change_unit,brand=brand,user_id=request.user.id)
            new_ing.save()
            return redirect('buy_ingredient')
    return render(request, 'buy_ingredient_form.html')


@login_required(login_url='login')
def Ingredient_two_form_template(request,id):
    if request.user.is_authenticated:
        drk = Drink.objects.filter(id=id).first()
        ing = Ingredient.objects.filter(user_id=request.user.id).all()
        if request.method == 'POST':
            ing_sel = request.POST.get('ing_select')
            value = request.POST.get('value')

            if drk:
                ig = Ingredient.objects.filter(id=ing_sel,user_id=request.user.id)
                real_price = int(value)/int(ig.change_value) * int(ig.price)
                new_ing = Ingredient2(name=ig.name,price=real_price,ing_id=ig.id,buy_unit=ig.buy_unit,change_unit=ig.change_unit,value=value,change_value=ig.change_value,main_drink=drk.name,main_drink_id=drk.id)
                new_ing.save()
                ing = Ingredient.objects.filter(id=ing_sel,user_id=request.user.id)
                s = 0
                for item in ing:
                    s += int(item.price)
                drk.total_ingredient = s
                drk.money = drk.price - s
                return redirect('Ingredient',id=id)
    return render(request, 'ingredient_form.html',{'ing':ing})


def thank(request):
    template = loader.get_template('thank.html')
    return HttpResponse(template.render())

def LoginPage(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        pass1 = request.POST.get('password')
        user2 = Info_user.objects.filter(phone=phone).first()
        if user2:
            user = authenticate(request,username=user2.name,password=pass1)
            if user:
                login(request,user)
                return redirect('home')
            else:
                return HttpResponse ("Username or Password is incorrect!!!")
        else:
            return redirect('a_login')

    return render (request,'registration/login.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        address = request.POST.get('address')
        q_name = request.POST.get('q_name')
        pass1=request.POST.get('password')
        user2 = Info_user.objects.filter(phone=phone).first()
        user = User.objects.filter(username=uname).first()
        if user:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            new_user = User.objects.filter(email=email).first()
            info = Info_user(name=new_user.username,phone=phone,q_name=q_name,address=address,join_date=new_user.date_joined,user_id=new_user.id)
            info.save()
            login(request,new_user)
            return redirect('home')
    return render (request,'registration/signup.html')


@login_required(login_url='a_login')
def LogoutPage(request):
    logout(request)
    return redirect('home')

@login_required(login_url='a_login')
def delete_drink(self,id):
    find = Drink.objects.filter(id=id).first()
    find.delete()
    return redirect('home')

@login_required(login_url='a_login')
def delete_drink_group(self,sid):
    Drink_group.objects.filter(id=sid).delete()
    return redirect('home')

@login_required(login_url='a_login')
def delete_ingredient(self,id):
    find = Ingredient.objects.filter(id=id).first()
    find.delete()
    return redirect('home')

@login_required(login_url='a_login')
def delete_ingredient2(self,id):
    find = Ingredient2.objects.filter(id=id).first()
    find.delete()
    return redirect('home')

def code():
    text = ''
    count = 0
    for i in range(1,7):
        text = text + str(random.randint(0,9))
        count += i
    return text

def change_password(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user = Info_user.objects.filter(phone=phone).first()
        user1 = User.objects.filter(id=user.user_id).first()
        if user1:
            text = code()
            phone = phone.replace('0','+84',1)
            message = client.messages.create(to=user.phone,from_=twilio_phone,body=text)
            message.sid
            return redirect(request,'check_sms',password=password,phone=phone,code=text)
    return render(request,'change_password.html')

def check_password_sms(password,phone,code,request):
    if request.method == 'POST':
        sms = request.POST.get('sms')
        if sms == code:
            user = Info_user.objects.filter(phone=phone).first()
            user1 = User.objects.filter(id=user.user_id).first()
            if user1:
                user1.password = password
                user1.save()
                login(request,user1)
                return redirect('home')
    return render(request,'sms.html')

@login_required(login_url='a_login')
def change_drink_group(request,id):
    if request.method == 'POST':
        name = request.POST.get('name')
        drink_g = Drink_group.objects.filter(id=id).first()
        drink_g.name = name
        drink_g.save()
        return redirect('drink_group')
    return render(request,'form.html')

@login_required(login_url='a_login')
def change_drink(request,id):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        group = request.POST.get('group')
        total_ingredient = request.POST.get('total_ingredient')
        money = request.POST.get('money')
        drink = Drink.objects.filter(id=id).first()
        drink.name = name
        drink.price = price
        drink.total_ingredient = total_ingredient
        drink.money = money
        drink_g = Drink_group.objects.filter(name=group).first()
        drink.group = group
        drink.group_id = drink_g.id
        drink.save()
        return redirect('home')
    return render(request,'form1.html')

@login_required(login_url='a_login')
def change_ingredient(request,id):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        buy_unit = request.POST.get('buy_unit')
        brand = request.POST.get('brand')
        ingredient = Ingredient.objects.filter(id=id).first()
        ingredient.name = name
        ingredient.price = price
        ingredient.buy_unit = buy_unit
        ingredient.brand = brand
        ingredient.save()
        return redirect('home')
    return render(request,'form2.html')

@login_required(login_url='a_login')
def change_ingredient2(request,id):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        value = request.POST.get('value')
        buy_unit = request.POST.get('buy_unit')
        change_unit = request.POST.get('change_unit')
        change_value = request.POST.get('change_value')
        brand = request.POST.get('brand')
        ingredient = Ingredient2.objects.filter(id=id).first()
        ingredient.name = name
        ingredient.price = price
        ingredient.buy_unit = buy_unit
        ingredient.value = value
        ingredient.change_value = change_value
        ingredient.change_unit = change_unit
        ingredient.brand = brand
        ingredient.save()
        return redirect('home')
    return render(request,'form3.html')

@login_required(login_url='a_login')
def caculator(request,id):
    ing = Ingredient2.objects.filter(main_drink_id=id).all()
    drk = Drink.objects.filter(id=id).first()
    if ing and drk:
        s = 0
        l = 0
        for item in ing:
            s += int(item.price)
        l = int(drk.price) - s
    context = {'sm':l,'s2':s,'drk':drk}
    return render(request,'caculate.html',context)

def admin_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=uname,password=password)
        if user is not None:
            login(request,user)
            return redirect('admin_check')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")
    return render(request,'admin_login.html')
