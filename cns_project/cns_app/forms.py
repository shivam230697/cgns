import uuid

from django import forms
from .models import RawMaterialModel, ProductionModel, InvoiceModel, Customer, PaymentModel
from address.forms import AddressField
from localflavor.in_.forms import INStateSelect
from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator


class IndexForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()


class RawMaterialForm(forms.ModelForm):
    rst_no = forms.IntegerField(min_value=0, required=True, error_messages={'required': 'RST is required field'})
    net_wt = forms.DecimalField(required=True, decimal_places=2,
                                error_messages={'required': 'Weight is required field'})

    rate = forms.DecimalField(
        required=True, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'required field'}),
        error_messages={'required': 'Rate is required field'}
    )
    kanta_rate = forms.DecimalField(decimal_places=2, max_digits=12, initial=100)
    paid_amount = forms.DecimalField(decimal_places=2, max_digits=12, required=True)




    class Meta:
        model = RawMaterialModel
        fields = "__all__"

class RawExpenseForm(forms.Form):
    from .environment import Environment
    env = Environment()
    type = forms.ChoiceField(choices=env.Raw_Expense_Choices, widget=forms.Select(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    expense_amount = forms.DecimalField(decimal_places=2, max_digits=12, widget=forms.TextInput(attrs={'class': 'form-control'}))


class ProductionForm(forms.ModelForm):
    product_rst = forms.IntegerField(required=True, error_messages={'required': 'RST Field is required'})
    vehicle_no = forms.CharField(required=False, max_length=10)
    product_net_weight = forms.DecimalField(decimal_places=2, error_messages={'required': 'Weight Field is required'})

    class Meta:
        model = ProductionModel
        fields = "__all__"

    class Media:
        js = ('js/auto_capitalize.js',)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class InvoiceForm(forms.Form):
    from .environment import Environment
    invoice_env = Environment()
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=True)

    total = forms.DecimalField(decimal_places=2, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    gst = forms.IntegerField()
    discount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False, initial=0)
    payment = forms.DecimalField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    item45mm = forms.BooleanField(label='Item 1', required=False,
                                  widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    item90mm = forms.BooleanField(label='Item 2', required=False,
                                  widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    item_pencil = forms.BooleanField(label='Item 3', required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    quantity_item1 = forms.DecimalField(label='Quantity for Item 1', required=False,
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    price_item1 = forms.DecimalField(label='Price for Item 1', required=False,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))

    quantity_item2 = forms.DecimalField(label='Quantity for Item 2', required=False,
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    price_item2 = forms.DecimalField(label='Price for Item 2', required=False,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))

    quantity_item3 = forms.DecimalField(label='Quantity for Item 3', required=False,
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    price_item3 = forms.DecimalField(label='Price for Item 3', required=False,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    shipping_address = forms.CharField(max_length=50)
    shipping_state = forms.ChoiceField(choices=invoice_env.STATE_CHOICES, label="Shipping State")
    shipping_city = forms.CharField(max_length=20)
    shipping_zip_code = forms.IntegerField()
    driver_name = forms.CharField(max_length=20, initial='UNKNOWN', required=True)
    driver_number = forms.IntegerField(initial=1234567890, required=True)
    assigned_vehicle = forms.CharField(max_length=10, initial='UNKNOWN', required=True)
    paid_amount = forms.DecimalField(max_digits=12, decimal_places=2, initial=0, required=True)


class CustomerForm(forms.Form):
    from .environment import Environment
    state_env = Environment()
    customer_name = forms.CharField()
    customer_number = forms.IntegerField()
    customer_address = forms.CharField()
    customer_state = forms.ChoiceField(choices=state_env.STATE_CHOICES)
    customer_city = forms.CharField(max_length=20)
    zip_code = forms.IntegerField(label='ZIP Code')
    customer_gstin = forms.CharField(max_length=20, required=True)
    # payment_status = forms.ChoiceField(choices=[('pending', 'PENDING'), ('paid', 'PAID')])
    # payment_dues = forms.DecimalField()


class PaymentForm(forms.Form):
    p_method = (
        ('cash', 'cash'),
        ('online', 'online'),
    )
    p_status = (
        ('paid', 'paid'),
        ('pending', 'pending'),
    )
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    payment_method = forms.ChoiceField(choices=p_method, label='payment method')
    payment_amount = forms.DecimalField()
    # payment_status = forms.ChoiceField(choices=p_status, label='Status')
    # payment_dues = forms.DecimalField(null=True, max_digits=12, editable=False, decimal_places=2)
