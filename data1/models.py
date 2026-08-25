# from asyncio.windows_events import NULL
from email.policy import default
from pickletools import decimalnl_long
from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from django.db import models
from django.utils.dates import MONTHS
from django.shortcuts import redirect,reverse
from django.contrib import admin


t_list=(("ಪಾಡ್ಯ","ಪಾಡ್ಯ"),("ದ್ವಿತೀಯ","ದ್ವಿತೀಯ"),("ತೃತೀಯ","ತೃತೀಯ"),("ಚತುರ್ಥಿ","ಚತುರ್ಥಿ"),("ಪಂಚಮಿ","ಪಂಚಮಿ"),("ಅಮಾವಾಸ್ಯೆ","ಅಮಾವಾಸ್ಯೆ"))
month_list=(("January","January"),("February","February"),("March","March"),("April","April"),("May","May"),("June","June"),("July","July"),)
# Create your models here.

class paksha(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class maasa(models.Model):
    name=models.CharField(max_length=100) 

    def __str__(self):
        return self.name
    
    def get_detail(self):
        return reverse("data1:detail",kwargs={'slug':self.name})

class thithi(models.Model):
    maasa=models.ForeignKey(maasa,on_delete=models.CASCADE)
    paksha=models.ForeignKey(paksha,on_delete=models.CASCADE)
    thithi=models.IntegerField()
    pooja_day=models.DateField(null=True)
    def __str__(self):
        return self.maasa.name+" "+self.paksha.name+" "+str(self.thithi)

    def get_detail(self):
        return reverse("data1:info",kwargs={'slug':self.id})    

class admin_model(admin.ModelAdmin):
    search_fields=('name',)

class user(models.Model):
    receipt_number=models.CharField(max_length=100)
    year=models.IntegerField()
    name=models.CharField(max_length=300)
    address=models.TextField()
    pincode=models.IntegerField()
    phone=models.BigIntegerField()
    is_hindu=models.BooleanField(default=True)
    thithi=models.ForeignKey(thithi,on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(blank=True,null=True,default='2000-01-01')
    amount=models.DecimalField(default=0,decimal_places=2,max_digits=11)
    i_amount=models.DecimalField(default=0,decimal_places=2,max_digits=11)
    address_not_found=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
 