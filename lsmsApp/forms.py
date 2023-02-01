from datetime import datetime
from tabnanny import check
from django import forms
from numpy import require
from lsmsApp import models
from django.db import transaction

import datetime


class SaveProducts(forms.ModelForm):
    product_type = forms.CharField(max_length=250)
    price = forms.CharField(max_length=250)
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Products
        fields = ('product_type', 'price', 'status', )

    def clean_product_type(self):
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        product_type = self.cleaned_data['product_type']
        try:
            if id > 0:
                product = models.Products.objects.exclude(id = id).get(product_type = product_type, delete_flag = 0)
            else:
                product = models.Products.objects.get(product_type = product_type, delete_flag = 0)
        except:
            return product_type
        raise forms.ValidationError("Product Type already exists.")


class SaveInvoice(forms.ModelForm):
    code = forms.CharField(max_length=250)
    client = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250,required= False)
    status = forms.CharField(max_length=2)
    payment = forms.CharField(max_length=2)
    total_amount = forms.CharField(max_length=250)
    amount_paid = forms.CharField(max_length=250)
    

    class Meta:
        model = models.Invoice
        fields = ('code', 'client', 'contact', 'status', 'payment', 'total_amount', 'amount_paid',)

    def clean_code(self):
        code = self.cleaned_data['code']
       
        if code == 'generate':
            pref = datetime.datetime.now().strftime('%y%m%d')
            code = 1
            while True:
                try:
                    check = models.Invoice.objects.get(code = f"{pref}{code:05d}")
                    code = code + 1
                except:
                    return f"{pref}{code:05d}"
                    break
        else:
            return code
    
    def clean_payment(self):
        amount_paid = float(self.data['amount_paid'])
        if amount_paid > 0:
            return 1
        else:
            return 0

    def save(self):
        instance = self.instance
        Products = []
  
        # print(f"{self.data}")
        if 'product_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('product_id[]')):
                product = models.Products.objects.get(id=val)
                price = self.data.getlist('product_price[]')[k]
                weight = self.data.getlist('product_weight[]')[k]
                total = float(price) * float(weight)
                try:
                    Products.append(models.InvoiceProducts(invoice = instance, product_type = product, price = price,weight = weight, total_amount = total))
                    print("InvoiceProducts..")
                except Exception as err:
                    print(err)
                    return False
        
        try:
            instance.save()
            models.InvoiceProducts.objects.filter(invoice = instance).delete()
            models.InvoiceProducts.objects.bulk_create(Products)            
        except Exception as err:
            print(err)
            return False


class SaveEmployeeProducts(forms.ModelForm):
    product_type = forms.CharField(max_length=250)
    price = forms.CharField(max_length=250)
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.EmployeeProducts
        fields = ('product_type', 'price', 'status', )
        exclude = ('employee_id',)

class SavePurchase(forms.ModelForm):
    code = forms.CharField(max_length=250)
    client = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250,required= False)
    status = forms.CharField(max_length=2)
    payment = forms.CharField(max_length=2)
    total_amount = forms.CharField(max_length=250)
    amount_paid = forms.CharField(max_length=250)
        
    class Meta:
        model = models.Purchase
        fields = ('code', 'client', 'contact', 'status', 'payment', 'total_amount', 'amount_paid',)
        exclude = ('employee_id',)

    def clean_code(self):
        code = self.cleaned_data['code']
       
        if code == 'generate':
            pref = datetime.datetime.now().strftime('%y%m%d')
            code = 1
            while True:
                try:
                    check = models.Purchase.objects.get(code = f"{pref}{code:05d}")
                    code = code + 1
                except:
                    return f"{pref}{code:05d}"
                    break
        else:
            return code
    
    def clean_payment(self):
        amount_paid = float(self.data['amount_paid'])
        if amount_paid > 0:
            return 1
        else:
            return 0

    def save(self):
        instance = self.instance
        Products = []
  
        # print(f"{self.data}")
        if 'product_id[]' in self.data:
            for k, val in enumerate(self.data.getlist('product_id[]')):
                product = models.EmployeeProducts.objects.get(id=val)
                price = self.data.getlist('product_price[]')[k]
                weight = self.data.getlist('product_weight[]')[k]
                total = float(price) * float(weight)
                try:
                    Products.append(models.PurchaseProducts(purchase = instance, product_type = product, price = price,weight = weight, total_amount = total))
                    print("PurchaseProducts..")
                except Exception as err:
                    print(err)
                    return False
        
        try:
            instance.save()
            models.PurchaseProducts.objects.filter(purchase = instance).delete()
            models.PurchaseProducts.objects.bulk_create(Products)            
        except Exception as err:
            print(err)
            return False

