from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Drink_group, Drink,Ingredient,Ingredient2,Info_user
from .forms import Ingredient_form
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

@login_required(login_url='login')
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

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
@login_required(login_url='login')
def Ingredient2_view(request,id):
    model = Ingredient2.objects.filter(main_drink_id=id).first()
    return render(request,'ingredient.html',{'posts':model})


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


@login_required(login_url='login')
def add_ingredient(request,id):
    buy_i = Ingredient.objects.filter(id=id).first()
    if request.method == 'POST':
        name = request.POST.get('name')
        change_value = request.POST.get('change_value')
        change_unit = request.POST.get('change_unit')
        value = request.POST.get('value')
        
        dr = Drink.objects.filter(name=name).first()
        dk = Ingredient2(name=buy_i.name,main_drink=dr.name,main_drink_id=dr.id,buy_unit=buy_i.buy_unit,price=int(value)/int(change_value)*int(buy_i.price),change_value=change_value,change_unit=change_unit,value=value)
        dk.save()
        return redirect('buy_ingredient')
    return render(request,'add_ingredient.html')

@method_decorator(login_required, name='dispatch')
class Info_user_view(generic.ListView):
    model = Info_user
    template_name = 'admin.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            add = Info_user.objects.all()
            return add[::-1]
        else:
            return redirect('home')

class DetailView5(generic.DetailView):
    model = Info_user

'''
def home(request):
    model = Course.objects.all()
    context = {'model':model}
    return render('home.html', context)
'''

@login_required(login_url='login')
def Drink_group_form_template(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if not Drink_group.objects.filter(name=name):
            dg = Drink_group(name=name)
            dg.save()
            dg = Drink_group.objects.filter(name=name).first()
            return redirect('drink_form',id=dg.id)
        else:
            return redirect('drink_group_form')
    return render(request, 'drink_group_form.html')

@login_required(login_url='login')
def Drink_form_template(request,id):
    drk = Drink_group.objects.filter(id=id).first()
    if request.method == 'POST':
        price = request.POST.get('price')
        name = request.POST.get('name')

        if drk:
            return redirect('create_drink',name=name,price=price,group=drk.name,group_id=drk.id)
    return render(request, 'drink_form.html')

@login_required(login_url='login')
def create_drink(self,name,price,group,group_id):
    new_ing = Drink(name=name,price=price,group=group,group_id=group_id) 
    new_ing.save()
    drk = Drink.objects.filter(name=name).first()
    return redirect('drink')

@login_required(login_url='login')
def add_drink_form(request):
    if request.method == 'POST':
        price = request.POST.get('price')
        name = request.POST.get('name')
        group_name = request.POST.get('group_name')

        drk = Drink_group.objects.filter(name=group_name).first()

        if drk:
            return redirect('create_drink',name=name,price=price,group=drk.name,group_id=drk.id)
    return render(request, 'add_drink_form.html')

@login_required(login_url='login')
def Ingredient_form_template(request):
    form = Ingredient_form()
    if request.method == 'POST':
        form = Ingredient_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('buy_ingredient'))
    context = {'form':form}
    return render(request, 'buy_ingredient_form.html', context)

'''
@login_required(login_url='login')
def Ingredient_two_form_template(request,id):
    drk = Drink.objects.filter(id=id).first()
    if request.method == 'POST':
        price = request.POST.get('price')
        name = request.POST.get('name')
        buy_unit = request.POST.get('buy_unit')
        change_value = request.POST.get('change_value')
        change_unit = request.POST.get('change_unit')
        value = request.POST.get('value')

        if drk:
            real_price = int(value)/int(change_value) * int(price)
            new_ing = Ingredient2(name=name,price=real_price,buy_unit=buy_unit,change_unit=change_unit,value=value,change_value=change_value,main_drink=drk.name,main_drink_id=id) 
            new_ing.save()
            return redirect('Ingredient',id=id)
    return render(request, 'ingredient_form.html')
'''

def thank(request):
    template = loader.get_template('thank.html')
    return HttpResponse(template.render())
    
def LoginPage(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        pass1 = request.POST.get('password')
        info = Info_user.objects.filter(phone=phone).first()
        user = authenticate(request,username=info.name,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        address = request.POST.get('address')
        q_name = request.POST.get('q_name')
        pass1=request.POST.get('password')
        user2 = Info_user.objects.filter(phone=phone).first()
        user = User.objects.filter(username=user2.username).first()
        if user:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            new_user = User.objects.filter(email=email)
            info = Info_user(name=new_user.username,phone=phone,q_name=q_name,address=address,join_date=new_user.date_joined)
            info.save()
            login(request,new_user)
            return redirect('home')
    return render (request,'signup.html')


@login_required(login_url='login')
def LogoutPage(request):
    logout(request)
    return redirect('home')
    
@login_required(login_url='login')
def delete_drink(self,id):
    find = Drink.objects.filter(id=id).first()
    find.delete()
    return redirect('home')

@login_required(login_url='login')
def delete_drink_group(self,sid):
    Drink_group.objects.filter(id=sid).delete()
    return redirect('home')

@login_required(login_url='login')
def delete_ingredient(self,id):
    find = Ingredient.objects.filter(id=id).first()
    find.delete()
    return redirect('home')

@login_required(login_url='login')
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

def change_password(request,id):
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

@login_required(login_url='login')
def change_drink_group(request,id):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name != None:
            drink_g = Drink_group.objects.filter(id=id).first()
            drink_g.name = name
            drink_g.save()
            return redirect('drink_group')
    return render(request,'form.html')

@login_required(login_url='login')
def change_drink(request,id):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        group = request.POST.get('group')
        drink = Drink.objects.filter(id=id).first()
        if name != None:
            drink.name = name
            drink.save()
        elif price != None:
            drink.price = price
            drink.save()
        elif group != None:
            drink_group = Drink_group.objects.filter(name=group).first()
            drink.group = group
            drink.group_id = drink_group.id
            drink.save()
        return redirect('home')
    return render(request,'form1.html')

@login_required(login_url='login')
def change_ingredient(request,id):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        buy_unit = request.POST.get('buy_unit')
        ingredient = Ingredient.objects.filter(id=id).first()
        if name != None:
            ingredient.name = name
            ingredient.save()
        elif price != None:
            ingredient.price = price
            ingredient.save()
        elif buy_unit != None:
            ingredient.buy_unit = buy_unit
            ingredient.save()
        return redirect('home')
    return render(request,'form2.html')

@login_required(login_url='login')
def change_ingredient2(request,id):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        value = request.POST.get('value')
        buy_unit = request.POST.get('buy_unit')
        change_unit = request.POST.get('change_unit')
        change_value = request.POST.get('change_value')
        ingredient = Ingredient2.objects.filter(id=id).first()
        if name != None:
            ingredient.name = name
            ingredient.save()
        elif price != None:
            ingredient.price = price
            ingredient.save()
        elif buy_unit != None:
            ingredient.buy_unit = buy_unit
            ingredient.save()
        elif value != None:
            ingredient.value = value
            ingredient.save()
        elif change_value != None:
            ingredient.change_value = change_value
            ingredient.save()
        elif change_unit != None:
            ingredient.change_unit = change_unit
            ingredient.save()
        return redirect('home')
    return render(request,'form3.html')

@login_required(login_url='login')
def caculator(request,id):
    ing = Ingredient2.objects.filter(main_drink_id=id).all()
    drk = Drink.objects.filter(id=id).first()
    if ing and drk:
        s = 0
        l = 0
        for item in ing:
            s += int(item.price)
        l = int(drk.price) - s
    return render(request,'caculate.html',sum=l,s2=drk,drk=drk)

def admin_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=uname,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")
    return render(request,'admin_login.html')
