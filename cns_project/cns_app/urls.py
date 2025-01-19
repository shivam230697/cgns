from django.urls import path

from . import views
from .views import user_login, user_logout, user_signup

urlpatterns = [
    path('', views.base, name="base"),
    path('index/', views.index, name="index"),
    path('raw_material/', views.raw_material, name="raw_material"),
    path('raw_material_details/', views.raw_material_view, name="raw_material_view"),
    path('raw_material_update/<int:pk>', views.raw_material_update, name="rm_update"),
    path('confirm/<int:pk>', views.confirm, name="confirm"),
    path('delete_rm/<int:pk>', views.delete_raw_material_entry, name="delete_rm_entry"),
    path('raw_expense/', views.raw_expense, name="raw_expense"),
    path('raw_expense_add/', views.raw_expense_add, name="raw_expense_add"),


    path('add_production/', views.add_production, name="add_production"),
    path('view_productions/', views.view_production, name="view_production"),
    path('edit_production/<int:pk>', views.edit_production, name="edit_production"),
    path('update_production/<int:pk>', views.update_production, name="update_production"),
    path('delete_production/<int:pk>', views.delete_production, name="delete_production"),
    path('dashboard_page/', views.dashboard, name="dashboard"),
    path('view_invoices/', views.view_invoices, name="view_invoices"),
    path('add_invoice/', views.add_invoice, name="add_invoice"),
    path('my_page/', views.my_page, name="my_page"),
    path('add_customer/', views.add_customer, name="add_customer"),
    path('customer_list/', views.view_customer, name="check_customer"),
    path('check_invoice/<int:invoice_id>', views.view_invoice, name="check_invoice"),
    path('payment_history/<int:customer_id>', views.payment_history, name="payment_history"),

    path('payment/', views.payment, name="payment"),
    path('view_payment/', views.view_payment, name="view_payments"),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('signup/', user_signup, name='signup'),

    path('get_customer_address/<int:customer_id>/', views.get_customer_address, name='get_customer_address'),

]
