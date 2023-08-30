from django import forms
from .models import Drink_group, Drink,Ingredient,Ingredient2

class Drink_group_form(forms.ModelForm):
    class Meta:
        model = Drink_group
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control shadow'}),
        }
        label = {
            'name':'Tên nhóm đồ uống',
        }
'''
class Drink_Form(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ['name','price', 'group']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control shadow'}),
            'price': forms.TextInput(attrs={'class':'form-control shadow'}),
            'group': forms.TextInput(attrs={'class':'form-control shadow'}),
        }
        label = {
            'name':'Tên đồ uống',
            'price':'Giá',
            'group':'Nhóm đồ uống'
        }
'''

class Ingredient2_form(forms.ModelForm):
    class Meta:
        model = Ingredient2
        fields = ['name','buy_unit','price','use_unit','brand']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control shadow'}),
            'buy_unit': forms.TextInput(attrs={'class':'form-control shadow'}),
            'price': forms.TextInput(attrs={'class':'form-control shadow'})
        }
        label = {
            'name':'Tên đồ uống',
            'buy_unit':'Đơn vị mua vào',
            'price':'Giá cả'
        }


'''
class Ingredient2_form(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name','buy_unit','price','change_value']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control shadow'}),
            'buy_unit': forms.TextInput(attrs={'class':'form-control shadow'}),
            'price': forms.TextInput(attrs={'class':'form-control shadow'}),
            'main_drink': forms.TextInput(attrs={'class':'form-control shadow'}),
            'value': forms.TextInput(attrs={'class':'form-control shadow'}),
            'change_value': forms.TextInput(attrs={'class':'form-control shadow'}),
            'change_unit': forms.TextInput(attrs={'class':'form-control shadow'})
        }
        label = {
            'name':'Tên đồ uống',
            'buy_unit':'Đơn vị mua vào',
            'change_unit':'Đơn vị pha chế',
            'change_value':'Giá trị đổi (VD: 1 DVM = ... DVPC)',
            'value':'Lượng cần để pha chế (theo đơn vị pha chế)',
            'price':'Giá nguyên liệu (theo lượng cần pha chế)',

        }
'''