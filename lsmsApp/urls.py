from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from .import Employee_Views
from .import Hod_Views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('base/', views.BASE, name="base"),
    # Login Path    
    path('', views.LOGIN, name="login"),
    path('dologin', views.dologin, name="dologin"),
    path('dologout', views.dologout, name='logout'),

    # Profile Update
    path('profile', views.PROFILE, name='profile'),
    path('profile/update', views.PROFILE_UPDATE, name='profile_update'),
    # This is Hod Panel Url
    path('Hod/home', Hod_Views.home,name='hod_home'),
    #Employee 
    path('Hod/Employee/Add', Hod_Views.ADD_EMPLOYEE, name="add_employee"),
    path('Hod/Employee/View', Hod_Views.VIEW_EMPLOYEE, name="view_employee"),
    path('Hod/Employee/Edit/<str:id>', Hod_Views.EDIT_EMPLOYEE, name="edit_employee"),
    path('Hod/Employee/Update', Hod_Views.UPDATE_EMPLOYEE, name="update_employee"),
    path('Hod/Employee/Delete/<str:admin>', Hod_Views.DELETE_EMPLOYEE, name="delete_employee"),
    #Products
    path('Hod/products', Hod_Views.products,name='product-page'),
    path('Hod/manage_product', Hod_Views.manage_product,name='manage-product'),
    path('Hod/manage_product/<int:pk>', Hod_Views.manage_product,name='manage-product-pk'),
    path('Hod/view_product', Hod_Views.view_product,name='view-product'),
    path('Hod/view_product/<int:pk>', Hod_Views.view_product,name='view-product-pk'),
    path('Hod/save_product', Hod_Views.save_product,name='save-product'),
    path('Hod/delete_product/<int:pk>', Hod_Views.delete_product,name='delete-product'),
    
    #invoices
    path('Hod/invoices', Hod_Views.invoices,name='invoice-page'),
    path('Hod/manage_invoice', Hod_Views.manage_invoice,name='manage-invoice'), 
    path('Hod/manage_invoice/<int:pk>', Hod_Views.manage_invoice,name='manage-invoice-pk'),
    path('Hod/view_invoice', Hod_Views.view_invoice,name='view-invoice'),
    path('Hod/view_invoice/<int:pk>', Hod_Views.view_invoice,name='view-invoice-pk'),
    path('Hod/save_invoice', Hod_Views.save_invoice,name='save-invoice'),
    path('Hod/delete_invoice/<int:pk>', Hod_Views.delete_invoice,name='delete-invoice'),
    path('Hod/update_transaction_form/<int:pk>', Hod_Views.update_transaction_form,name='transaction-update-status'),
    path('Hod/update_transaction_status', Hod_Views.update_transaction_status,name='update-invoice-status'),
    path('Hod/daily_report', Hod_Views.daily_report,name='daily-report'),
    path('Hod/daily_report/<str:date>', Hod_Views.daily_report,name='daily-report-date'),

    #Expenses
    path('Hod/Expense/Add', Hod_Views.ADD_EXPENSE, name="add_expense"),
    path('Hod/Expense/View', Hod_Views.VIEW_EXPENSE, name="view_expense"),
    path('Hod/Expense/Edit/<str:id>', Hod_Views.EDIT_EXPENSE, name="edit_expense"),
    path('Hod/Expense/Update', Hod_Views.UPDATE_EXPENSE, name="update_expense"),
    path('Hod/Expense/Delete/<str:id>', Hod_Views.DELETE_EXPENSE, name="delete_expense"),


    # Employee urls
    path('Employee/Home', Employee_Views.HOME, name="employee_home"),
    #Products
    path('Employee/products_employee', Employee_Views.products_employee,name='product-employee-page'),
    path('Employee/manage_employee_product', Employee_Views.manage_employee_product,name='manage-employee-product'),
    path('Employee/manage_employee_product/<int:pk>', Employee_Views.manage_employee_product,name='manage-employee-product-pk'),
    path('Employee/view_employee_product/<int:pk>', Employee_Views.view_employee_product,name='view-employee-product-pk'),
    path('Employee/save_employee_product', Employee_Views.save_employee_product,name='save-employee-product'),
    path('Employee/delete_employee_product/<int:pk>', Employee_Views.delete_employee_product,name='delete-employee-product'),

    path('Employee/purchases', Employee_Views.purchases,name='purchase-page'),
    path('Employee/manage_purchase', Employee_Views.manage_purchase,name='manage-purchase'), 
    path('Employee/manage_purchase/<int:pk>', Employee_Views.manage_purchase,name='manage-purchase-pk'),
    path('Employee/view_purchase', Employee_Views.view_purchase,name='view-purchase'),
    path('Employee/view_purchase/<int:pk>', Employee_Views.view_purchase,name='view-purchase-pk'),
    path('Employee/save_purchase', Employee_Views.save_purchase,name='save-purchase'),
    path('Employee/delete_purchase/<int:pk>', Employee_Views.delete_purchase,name='delete-purchase'),
    path('Employee/update_transaction_form/<int:pk>', Employee_Views.update_transaction_form,name='transacton-update-status'),
    path('Employee/update_transaction_status', Employee_Views.update_transaction_status,name='update-purchase-status'),    

    path('Employee/purchase_daily_report', Employee_Views.purchase_daily_report, name='purchase-daily-report'),
    path('Employee/purchase_daily_report/<str:date>', Employee_Views.purchase_daily_report,name='purchase-daily-report-date'),

    #Costs
    path('Employee/Cost/Add', Employee_Views.ADD_COST, name="add_cost"),
    path('Employee/Cost/View', Employee_Views.VIEW_COST, name="view_cost"),
    path('Employee/Cost/Edit/<str:id>', Employee_Views.EDIT_COST, name="edit_cost"),
    path('Employee/Cost/Update', Employee_Views.UPDATE_COST, name="update_cost"),
    path('Employee/Cost/Delete/<str:id>', Employee_Views.DELETE_COST, name="delete_cost"),


]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
