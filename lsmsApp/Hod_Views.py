import datetime
from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from lsmsApp import models, forms
from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
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
    
@login_required
def home(request):
    context = context_data(request)
    context['page'] = 'home'
    context['page_title'] = 'Home'
    
    date = datetime.datetime.now()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    context['employees'] = models.Employee.objects.all().count()
    context['products'] = models.Products.objects.filter(delete_flag = 0).count()
    context['todays_invoice'] = models.Invoice.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).count()
    context['todays_achat'] = models.Invoice.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).aggregate(Sum('amount_paid'))['amount_paid__sum']

    bottle_count = models.InvoiceProducts.objects.filter(product_type__product_type='Bottle').aggregate(
        pur_bottle=Sum('weight')
    )
    context['bottle_count'] = int(bottle_count['pur_bottle'])
    boite_count = models.InvoiceProducts.objects.filter(product_type__product_type='Boite').aggregate(
        pur_boite=Sum('weight')
    )
    context['boite_count'] = int(boite_count['pur_boite'])
    carduna_count = models.InvoiceProducts.objects.filter(product_type__product_type='Carduna').aggregate(
        pur_carduna=Sum('weight')
    )
    context['carduna_count'] = int(carduna_count['pur_carduna'])

    #Expences
    
    context['bessim_expenses'] = models.Expenses.objects.filter(
        employee__admin__username='Bessim Mkouar',
        date_added__year = year,
        date_added__month = month,
        date_added__day = day,
        ).aggregate(Sum('amount'))['amount__sum']

    context['chokri_expenses'] = models.Expenses.objects.filter(
        employee__admin__username='Chokri Douma',
        date_added__year = year,
        date_added__month = month,
        date_added__day = day,
        ).aggregate(Sum('amount'))['amount__sum']


    #Rest
    context['todays_purchases'] = models.Purchase.objects.filter(
            employee_id__admin__username = 'Bessim Mkouar',
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).aggregate(Sum('amount_paid'))['amount_paid__sum']

    context['costs'] = models.Costs.objects.filter(
        employee_id__admin__username = 'Bessim Mkouar',
        date_added__year = year,
        date_added__month = month,
        date_added__day = day,
        ).aggregate(Sum('amount'))['amount__sum']

    context['expenses'] = models.Expenses.objects.filter(
        employee__admin__username = 'Bessim Mkouar',
        date_added__year = year,
        date_added__month = month,
        date_added__day = day,
        ).aggregate(Sum('amount'))['amount__sum']

    context['bessim_rest'] = None

    if context['todays_purchases'] and context['costs'] and  context['expenses'] is not None:
        context['bessim_rest'] = int(context['expenses']) - (int(context['todays_purchases']) + int(context['costs']))  
    elif context['expenses'] and context['todays_purchases'] is not None:
        context['bessim_rest'] = int(context['expenses']) - int(context['todays_purchases'])
    elif context['expenses'] and context['costs'] is not None:
        context['bessim_rest'] = int(context['expenses']) - int(context['costs'])
    elif context['todays_purchases'] and context['costs'] is not None:
        context['bessim_rest'] = int(context['todays_purchases']) + int(context['costs'])
    elif context['expenses'] is not None:
        context['bessim_rest'] = int(context['expenses'])          
    else:
        context['bessim_rest']=0

    context['todays_purchases'] = models.Purchase.objects.filter(
            employee_id__admin__username = 'Chokri Douma',
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
    ).aggregate(Sum('amount_paid'))['amount_paid__sum']

    context['costs'] = models.Costs.objects.filter(
        employee_id__admin__username = 'Chokri Douma',
        date_added__year = year,
        date_added__month = month,
        date_added__day = day,
        ).aggregate(Sum('amount'))['amount__sum']

    context['expenses'] = models.Expenses.objects.filter(
        employee__admin__username = 'Chokri Douma',
        date_added__year = year,
        date_added__month = month,
        date_added__day = day,
        ).aggregate(Sum('amount'))['amount__sum']

    context['chokri_rest'] = None

    if context['todays_purchases'] and context['costs'] and  context['expenses'] is not None:
        context['chokri_rest'] = int(context['expenses']) - (int(context['todays_purchases']) + int(context['costs']))  
    elif context['expenses'] and context['todays_purchases'] is not None:
        context['chokri_rest'] = int(context['expenses']) - int(context['todays_purchases'])
    elif context['expenses'] and context['costs'] is not None:
        context['chokri_rest'] = int(context['expenses']) - int(context['costs'])
    elif context['todays_purchases'] and context['costs'] is not None:
        context['chokri_rest'] = int(context['todays_purchases']) + int(context['costs'])
    elif context['expenses'] is not None:
        context['chokri_rest'] = int(context['expenses'])          
    else:
        context['chokri_rest']=0    

    #Monthly Expenses
    context['bessim_report'] = models.Expenses.objects.filter(
        employee__admin__username='Bessim Mkouar',
        ).annotate(month=TruncMonth('date_added')).values('month').aggregate(Sum('amount'))['amount__sum']
    context['chokri_report'] = models.Expenses.objects.filter(
        employee__admin__username='Chokri Douma',
        ).annotate(month=TruncMonth('date_added')).values('month').aggregate(Sum('amount'))['amount__sum']
    

    return render(request, 'Hod/hod_home.html', context)



def ADD_EMPLOYEE(request):
    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')

        if models.CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Is Already Taken')
            return redirect('add_employee')

        gender = request.POST.get('gender')
        if models.CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Is Already Taken')
            return redirect('add_employee')    

        else:
            user = models.CustomUser(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username=username,
               
                user_type = 2,

            )
            user.set_password(password)
            user.save()

            employee = models.Employee(
                admin=user,
                address = address,
                gender = gender,
            )
            employee.save()
            messages.success(request, 'Employee Are Successfully Added')
            return redirect('view_employee')

    
    return redirect('view_employee')


def VIEW_EMPLOYEE(request):
    
    employee = models.Employee.objects.all()

    context = {
        'employee': employee,
    }
    return render(request, 'Hod/view_employee.html', context)


def EDIT_EMPLOYEE(request, id):
    employee = models.Employee.objects.get(id=id)
    
    context = {
        'employee': employee,
    }

    return render(request, 'Hod/edit_employee.html', context)


def UPDATE_EMPLOYEE(request):
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')

        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = models.CustomUser.objects.get(id=employee_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic    
        user.save()

        employee = models.Employee.objects.get(admin=employee_id)
        employee.address = address
        employee.gender = gender
        employee.save()
        messages.success(request, 'Employee Is Successfully Updated')
        return redirect('view_employee')


    return render(request, 'Hod/edit_employee.html')


def DELETE_EMPLOYEE(request, admin):
    
    employee = models.Employee.objects.get(id=admin)
    employee.delete()
    messages.success(request, 'Employee Are Deleted Successfully')
   
    return redirect('view_employee')


@login_required
def products(request):
    context = context_data(request)
    context['page'] = 'Product'
    context['page_title'] = "Product List"
    context['products'] = models.Products.objects.filter(delete_flag = 0).all()
    return render(request, 'Hod/products.html', context)

@login_required
def save_product(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            product = models.Products.objects.get(id = post['id'])
            form = forms.SaveProducts(request.POST, instance=product)
        else:
            form = forms.SaveProducts(request.POST) 

        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Product has been saved successfully.") 
                pid = models.Products.objects.last().id
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

@login_required
def view_product(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_product'
    context['page_title'] = 'View Product'
    if pk is None:
        context['product'] = {}        
    else:
        context['product'] = models.Products.objects.get(id=pk)
       
    
    return render(request, 'Hod/view_product.html', context)

@login_required
def manage_product(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_product'
    context['page_title'] = 'Manage product'
    if pk is None:
        context['product'] = {}
    else:
        context['product'] = models.Products.objects.get(id=pk)
    
    return render(request, 'Hod/manage_product.html', context)

@login_required
def delete_product(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Product ID is invalid'
    else:
        try:
            models.Products.objects.filter(pk = pk).update(delete_flag = 1)
            messages.success(request, "Product has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Product Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def invoices(request):
    context = context_data(request)
    context['page'] = 'invoice'
    context['page_title'] = "invoice List"
    context['invoices'] = models.Invoice.objects.order_by('-date_added').all()
    return render(request, 'Hod/invoices.html', context)

@login_required
def save_invoice(request):
    resp = { 'status': 'failed', 'msg' : '', 'id': '' }
    if request.method == 'POST':
        post = request.POST
        if not post['id'] == '':
            invoice = models.Invoice.objects.get(id = post['id'])
            form = forms.SaveInvoice(request.POST, instance=invoice)
        else:
            form = forms.SaveInvoice(request.POST) 
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Invoice has been saved successfully.")
                pid = models.Invoice.objects.last().id
                resp['id'] = pid
            else:
                messages.success(request, "Invoice has been updated successfully.")
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

@login_required
def view_invoice(request, pk = None):
    context = context_data(request)
    context['page'] = 'view_invoice'
    context['page_title'] = 'View Invoice'
    if pk is None:
        context['invoice'] = {}
        context['pitems'] = {}
    else:
        context['invoice'] = models.Invoice.objects.get(id=pk)
        context['pitems'] = models.InvoiceProducts.objects.filter(invoice__id = pk).all()
    
    return render(request, 'Hod/view_invoice.html', context)

@login_required
def manage_invoice(request, pk = None):
    context = context_data(request)
    context['page'] = 'manage_invoice'
    context['page_title'] = 'Manage invoice'
    context['products'] = models.Products.objects.filter(delete_flag = 0, status = 1).all()

    if pk is None:
        context['invoice'] = {}
        context['pitems'] = {}
    else:
        context['invoice'] = models.Invoice.objects.get(id=pk)
        context['pitems'] = models.InvoiceProducts.objects.filter(invoice__id = pk).all()
    
    return render(request, 'Hod/manage_invoice.html', context)

@login_required
def update_transaction_form(request, pk = None):
    context = context_data(request)
    context['page'] = 'update_invoice'
    context['page_title'] = 'Update Transaction'
    if pk is None:
        context['invoice'] = {}
    else:
        context['invoice'] = models.Invoice.objects.get(id=pk)
    
    return render(request, 'Hod/update_status.html', context)

@login_required
def update_transaction_status(request):
    resp = { 'status' : 'failed', 'msg':''}
    if request.POST['id'] is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            models.Invoice.objects.filter(pk = request.POST['id']).update(status = request.POST['status'])
            messages.success(request, "Transaction Status has been updated successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Transaction Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_invoice(request, pk = None):
    resp = { 'status' : 'failed', 'msg':''}
    if pk is None:
        resp['msg'] = 'Invoice ID is invalid'
    else:
        try:
            models.Invoice.objects.filter(pk = pk).delete()
            messages.success(request, "Invoice has been deleted successfully.")
            resp['status'] = 'success'
        except:
            resp['msg'] = "Deleting Invoice Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")


def ADD_EXPENSE(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        amount = request.POST.get('amount')
        employee = models.Employee.objects.get(id=employee_id)
        
        expense = models.Expenses(
            employee = employee,
            amount = amount,                            
        )
        
        expense.save()
        messages.success(request, 'Expense Are Successfully Added')
        return redirect('view_expense')
    return render(request, 'Hod/add_expense.html')

def VIEW_EXPENSE(request):
    expense = models.Expenses.objects.all()
    employee = models.Employee.objects.all()
    context = {
        'expense': expense,
        'employee': employee,
    }
    return render(request, 'Hod/view_expense.html', context)

def EDIT_EXPENSE(request, id):
    expense = models.Expenses.objects.get(id=id)
    employee = models.Employee.objects.all()
    context = {
        'expense': expense,
        'employee': employee,
    }   
    return render(request, 'Hod/edit_expense.html', context)

def UPDATE_EXPENSE(request):
    if request.method == 'POST':
        expense_id = request.POST.get('expense_id')
        amount = request.POST.get('amount')
        employee_id = request.POST.get('employee_id')
        employee = models.Employee.objects.get(id=employee_id)    
        expense = models.Expenses(
            id = expense_id,
            employee = employee,
            amount = amount,
        )
        expense.save()
        messages.success(request, 'Expense Are Successfully Updated')
        return redirect('view_expense')

def DELETE_EXPENSE(request, id):
    expense = models.Expenses.objects.get(id=id)
    expense.delete()
    messages.success(request, 'Expense Are Successfully Deleted')
    return redirect('view_expense')

@login_required
def daily_report(request, date = None):
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
    context['invoices'] = models.Invoice.objects.filter(
            date_added__year = year,
            date_added__month = month,
            date_added__day = day,
        )   
    grand_total = 0
    for invoice in context['invoices']:
        grand_total += float(invoice.total_amount)
    context['grand_total'] = grand_total
    
    return render(request, 'Hod/report.html', context)