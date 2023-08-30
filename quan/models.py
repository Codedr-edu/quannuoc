from django.db import models

# Create your models here.
class Drink_group(models.Model):
    name = models.CharField(max_length=300)
    user_id = models.IntegerField()

class Drink(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField()
    group = models.CharField(max_length=300)
    group_id = models.IntegerField()
    total_ingredient = models.IntegerField()
    money = models.IntegerField()
    user_id = models.IntegerField()

class Ingredient2(models.Model):
    name = models.CharField(max_length=300)
    use_unit = models.CharField(max_length=300)
    price = models.IntegerField()
    value = models.IntegerField()
    ing_id = models.IntegerField()
    brand = models.CharField(max_length=300)
    main_drink = models.CharField(max_length=100)
    main_drink_id = models.IntegerField()
    user_id = models.IntegerField()

class Ingredient(models.Model):
    name = models.CharField(max_length=300)
    change_value = models.IntegerField()
    buy_value = models.IntegerField()
    buy_unit = models.CharField(max_length=100)
    change_unit = models.CharField(max_length=100)
    brand = models.CharField(max_length=300)
    price = models.IntegerField()
    user_id = models.IntegerField()

class Info_user(models.Model):
    name = models.CharField(max_length=1000)
    phone = models.CharField(max_length=1000)
    q_name = models.CharField(max_length=1500)
    address = models.CharField(max_length=10000)
    user_id = models.IntegerField()
    join_date = models.DateTimeField(auto_now_add=True,editable=False)