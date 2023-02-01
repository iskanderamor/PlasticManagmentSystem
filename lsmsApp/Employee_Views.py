import datetime
from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from lsmsApp import models, forms
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required

def context_data(request):
    fullpath = request.get_full_path()
    abs_uri = request.build_absolute_uri()
    abs_uri = abs_uri.split(fullpath)[0]
    context = {
        'system_host' : abs_uri,
        'page_name' : '',
        'page_title' : '',
        'system_name' : 'Plastic Company',
        
        'topbar' : True,
        'footer' : True,
    }

    return context

@login_required(login_url='/')
def HOME(request):
    context = context_data(request)
    context['page'] = 'home'
    context['page_title'] = 'Home'
    date = datetime.datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    employee_id = models.Employee.objects.get(admin=request.user.id)
    context['products'] = models.EmployeeProducts.objects.filter(employee_id=employee_id, delete_flag = 0).count()
    context['todays_invoice'] = models.Purchase.objects.filter(
            employee_id = employee_id,
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).count()
    context['todays_purchases'] = models.Purchase.objects.filter(
            employee_id = employee_id,
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).aggregate(Sum('amount_paid'))['amount_paid__sum']

    context['costs'] = models.Costs.objects.filter(
        employee_id=employee_id,
        date_added__year = year,
        date_added__month = month,
        date_added__day = day,
        ).aggregate(Sum('amount'))['amount__sum']

    context['expenses'] = models.Expenses.objects.filter(
        employee=employee_id,
        date_added__year = year,
        date_added__month = month,
        date_added__day = day,
        ).aggregate(Sum('amount'))['amount__sum']

    context['rest'] = None

    if context['todays_purchases'] and context['costs'] and  context['expenses'] is not None:
        context['rest'] = int(context['expenses']) - (int(context['todays_purchases']) + int(context['costs']))  
    elif context['expenses'] and context['todays_purchases'] is not None:
        context['rest'] = int(context['expenses']) - int(context['todays_purchases'])
    elif context['expenses'] and context['costs'] is not None:
        context['rest'] = int(context['expenses']) - int(context['costs'])
    elif context['todays_purchases'] and context['costs'] is not None:
        context['rest'] = int(context['todays_purchases']) + int(context['costs'])
    elif context['expenses'] is not None:
        context['rest'] = int(context['expenses'])          
    else:
        context['rest']=0

    #All Products
    context['bottle_sale'] = models.InvoiceProducts.objects.filter(
        invoice__client = 'Bessim Mkouar',
        product_type__product_type = 'Bottle',
    ).aggregate(Sum('weight'))['weight__sum']
    print(context['bottle_sale'])


    context['tot_bottle'] = 0
    context['bottle_count'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='Bottle'
        ).aggregate(Sum('weight'))['weight__sum']
    if context['bottle_count'] is not None:
        context['tot_bottle'] = int(context['bottle_count'])
    else:
        context['tot_bottle']=0            
    
    context['boite_count'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='Boite'
        ).aggregate(Sum('weight'))['weight__sum']
    if context['boite_count'] is not None:
        context['tot_boite'] = int(context['boite_count'])
    else:
        context['tot_boite']=0            

    context['carduna_bottle'] = 0
    context['carduna_count'] = models.PurchaseProducts.objects.filter(
        purchase__employee_id=employee_id,        
        product_type__product_type='Carduna'
        ).aggregate(Sum('weight'))['weight__sum']
    if context['carduna_count'] is not None:
        context['tot_carduna'] = int(context['carduna_count'])
    else:
        context['tot_carduna']=0            
    
   
      
    return render(request, 'Employee/employee_home.html', context)

@login_required(login_url='/')
def products_employee(request):
    context = context_data(request)
    context['page'] = 'Product'
    context['page_title'] = "Product List"
    employee_id = models.Employee.objects.get(admin=request.user.id)
    context['employeeproducts'] = models.EmployeeProducts.objects.filter(employee_id=employee_id).all()
    return render(request, 'Employee/products_employee.html', context)

@login_required(login_url='/')
def save_employee_product(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            employeeproduct = models.EmployeeProducts.objects.get(id = post['id'])
            form = forms.SaveEmployeeProducts(request.POST, instance=employeeproduct)
        else:
            form = forms.SaveEmployeeProducts(request.POST) 

        if form.is_valid():
            obj=form.save()
            obj.employee_id = models.Employee.objects.get(admin=request.user.id)
            obj.save()
            if post['id'] == '':
                messages.success(request, "Product has been saved successfully.") 
                pid = models.EmployeeProducts.objects.last().id
                resp['id'] = pid               
            else:
                messages.success(request, "Product has been updated successfully.")
                resp['id'] = post['id']
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required(login_url='/')
def view_employee_product(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_product'
    context['page_title'] = 'View Product'
    if pk is None:
        context['employeeproduct'] = {}        
    else:
        context['employeeproduct'] = models.EmployeeProducts.objects.get(id=pk)
       
    
    return render(request, 'Employee/view_employee_product.html', context)

@login_required(login_url='/')
def manage_employee_product(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_product'
    context['page_title'] = 'Manage product'
    if pk is None:
        context['employeeproduct'] = {}
    else:
        context['employeeproduct'] = models.EmployeeProducts.objects.get(id=pk)
    
    return render(request, 'Employee/manage_employee_product.html', context)

@login_required(login_url='/')
def delete_employee_product(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Product ID is invalid'
    else:
        try:
            models.EmployeeProducts.objects.filter(pk = pk).delete()
            messages.success(request, "Product has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Product Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")    

@login_required(login_url='/')
def purchases(request):
    context = context_data(request)
    context['page'] = 'purchase'
    context['page_title'] = "Purchase List"
    employee_id = models.Employee.objects.get(admin=request.user.id)
    context['purchases'] = models.Purchase.objects.filter(employee_id=employee_id).order_by('-date_added').all()
    return render(request, 'Employee/purchases.html', context)

@login_required(login_url='/')
def save_purchase(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            purchase = models.Purchase.objects.get(id = post['id'])
            form = forms.SavePurchase(request.POST, instance=purchase)
        else:
            form = forms.SavePurchase(request.POST) 
        if form.is_valid():
            form.instance.employee_id = models.Employee.objects.get(admin=request.user.id)
            form.save()
            
            if post['id'] == '':
                messages.success(request, "Purchase has been saved successfully.")
                pid = models.Purchase.objects.last().id
                resp['id'] = pid
            else:
                messages.success(request, "Purchase has been updated successfully.")
                resp['id'] = post['id']
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
         resp['msg'] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required(login_url='/')
def view_purchase(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_purchase'
    context['page_title'] = 'View Purchase'
    if pk is None:
        context['purchase'] = {}
        context['pitems'] = {}
    else:
        context['purchase'] = models.Purchase.objects.get(id=pk)
       
        context['pitems'] = models.PurchaseProducts.objects.filter(purchase__id = pk).all()
    
    return render(request, 'Employee/view_purchase.html', context)

@login_required(login_url='/')
def manage_purchase(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_purchase'
    context['page_title'] = 'Manage purchase'
    employee_id = models.Employee.objects.get(admin=request.user.id)
    context['products'] = models.EmployeeProducts.objects.filter(employee_id=employee_id, delete_flag = 0, status = 1).all()

    if pk is None:
        context['purchase'] = {}
        context['pitems'] = {}
    else:
        context['purchase'] = models.Purchase.objects.get(id=pk)
        context['pitems'] = models.PurchaseProducts.objects.filter(purchase__id = pk).all()
    
    return render(request, 'Employee/manage_purchase.html', context)

@login_required(login_url='/')
def update_transaction_form(request, pk = None):
    context = context_data(request)
    context['page'] = 'update_purchase'
    context['page_title'] = 'Update Transaction'
    if pk is None:
        context['purchase'] = {}
    else:
        context['purchase'] = models.Purchase.objects.get(id=pk)
    
    return render(request, 'Employee/update_status.html', context)    

@login_required(login_url='/')
def update_transaction_status(request):
    resp = { 'status' : 'failed', 'msg':''}
    if request.POST['id'] is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            models.Purchase.objects.filter(pk = request.POST['id']).update(status = request.POST['status'])
            messages.success(request, "Transaction Status has been updated successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Transaction Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")    

@login_required(login_url='/')
def delete_purchase(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Purchase ID is invalid'
    else:
        try:
            models.Purchase.objects.filter(pk = pk).delete()
            messages.success(request, "Purchase has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Purchase Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required(login_url='/')
def purchase_daily_report(request, date = None):
    context = context_data(request)
    context['page'] = 'view_invoice'
    context['page_title'] = 'Daily Transaction Report'
    
    if date is None:
        date = datetime.datetime.now()
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')
    else:
        date =datetime.datetime.strptime(date, '%Y-%m-%d')
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')

    context['date'] = date
    employee_id = models.Employee.objects.get(admin=request.user.id)
    context['purchases'] = models.Purchase.objects.filter(
            employee_id = employee_id,
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
        )
    grand_total = 0
    for purchase in context['purchases']:
        grand_total += float(purchase.total_amount)
    context['grand_total'] = grand_total
    
    return render(request, 'Employee/purchase_report.html', context)

@login_required(login_url='/')
def ADD_COST(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        employee = models.Employee.objects.get(admin=request.user.id)
        cost = models.Costs(
            employee_id = employee,
            description = description,
            amount = amount,
        )
        cost.save()
        messages.success(request, 'Cost Are Successfully Added')
        return redirect('view_cost')
    return render(request, 'Employee/add_cost.html')

@login_required(login_url='/')
def VIEW_COST(request):
    employee_id = models.Employee.objects.get(admin=request.user.id)
    cost = models.Costs.objects.filter(employee_id=employee_id)
    context = {
        'cost': cost, 
    }
    return render(request, 'Employee/view_cost.html', context)

@login_required(login_url='/')
def EDIT_COST(request, id):
    cost = models.Costs.objects.get(id=id)
    context = {
        'cost': cost,
    }
    return render(request, 'Employee/edit_cost.html', context)

@login_required(login_url='/')
def UPDATE_COST(request):
    if request.method == 'POST':
        cost_id = request.POST.get('cost_id')
        employee = models.Employee.objects.get(admin=request.user.id)
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        cost = models.Costs(
            id = cost_id,
            employee_id = employee,
            description = description,
            amount = amount,
        )
        cost.save()
        messages.success(request, 'Cost Are Successfully Updated')
        return redirect('view_cost')
    return render(request, 'Employee/edit_cost.html')

@login_required(login_url='/')
def DELETE_COST(request, id):
    cost = models.Costs.objects.get(id=id)
    cost.delete()
    messages.success(request, 'Cost Are Successfully Deleted')
    return redirect('view_cost')
    