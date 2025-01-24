from datetime import datetime
import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator
from address.models import AddressField
import pytz


# Create your models here.
class RawMaterialModel(models.Model):
    rst_no = models.IntegerField(unique=True)
    net_wt = models.DecimalField(max_digits=12, decimal_places=2)
    rate = models.DecimalField(max_digits=12, decimal_places=2)
    kanta_rate = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)

    total = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Other fields for your model
    @property
    def created_at_local(self):
        # Convert UTC time to local time
        local_tz = timezone.get_current_timezone()
        return self.created_at.astimezone(local_tz)

    def save(self, *args, **kwargs):
        # Update the 'updated_at' field every time the model is saved
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

class RawExpenseModel(models.Model):
    from .environment import Environment
    env = Environment()
    raw_choice = env.Raw_Expense_Choices
    expense_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=raw_choice)
    description = models.TextField()
    expense_amount = models.DecimalField(decimal_places=2, max_digits=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def created_at_local(self):
        # Convert UTC time to local time
        local_tz = timezone.get_current_timezone()
        return self.created_at.astimezone(local_tz)

    def save(self, *args, **kwargs):
        # Update the 'updated_at' field every time the model is saved
        self.description = str(self.description).capitalize()
        self.type = str(self.type).upper()
        super().save(*args, **kwargs)

class ProductionModel(models.Model):
    product_rst = models.IntegerField(unique=True)
    vehicle_no = models.CharField(blank=True, null=True, max_length=10,  default="UNKNOWN")
    product_net_weight = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Other fields for your model
    @property
    def created_at_local(self):
        # Convert UTC time to local time
        local_tz = timezone.get_current_timezone()
        return self.created_at.astimezone(local_tz)

    def save(self, *args, **kwargs):
        # Update the 'updated_at' field every time the model is saved
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add additional fields if needed (e.g., profile picture, etc.)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    from .environment import Environment
    env = Environment
    customer_name = models.CharField(max_length=20)
    customer_number = models.CharField(max_length=50)
    customer_address = models.CharField(max_length=100)
    customer_state = models.CharField(max_length=20, choices=env.STATE_CHOICES)
    customer_city = models.CharField(max_length=20)
    customer_gstin = models.CharField(max_length=20)
    zip_code = models.PositiveIntegerField()
    customer_state_code = models.CharField(max_length=3)
    payment_dues = models.DecimalField(null=True, max_digits=12, editable=False, decimal_places=2)
    payment_status = models.CharField(max_length=20, editable=False, choices=env.PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name

    @property
    def created_at_local(self):
        # Convert UTC time to local time
        local_tz = timezone.get_current_timezone()
        return self.created_at.astimezone(local_tz)

    def save(self, *args, **kwargs):
        self.customer_name = self.customer_name.upper()
        self.customer_city = self.customer_city.upper()

        # Call the original save method
        super().save(*args, **kwargs)


class InvoiceModel(models.Model):
    from .environment import Environment
    fg_env = Environment()
    invoice_id = models.CharField(max_length=20, editable=False, unique=True)
    invoice_number = models.IntegerField(blank=False, null=False, unique=True)
    e_way_bill = models.CharField(max_length=50 , unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    item_45mm = models.BooleanField(default=False, blank=True, null=True)
    item_90mm = models.BooleanField(default=False, blank=True, null=True)
    item_pencil = models.BooleanField(default=False, blank=True, null=True)
    item_45mm_quantity = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
    item_pencil_quantity = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
    item_90mm_quantity = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
    item_45mm_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    item_90mm_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    item_pencil_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_45mm = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_90mm = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_pencil = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    item_type = models.CharField(max_length=50, choices=fg_env.item_choices, default='None')
    item_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    item_rate = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(null=True, max_digits=12, editable=False, decimal_places=2)
    gst = models.IntegerField()
    discount = models.IntegerField(default=0, blank=True, null=True)
    payment = models.DecimalField(null=True, max_digits=12, editable=False, decimal_places=2)
    shipping_address = models.CharField(max_length=50)
    shipping_state = models.CharField(max_length=20, choices=fg_env.STATE_CHOICES)
    shipping_state_code = models.CharField(max_length=3)
    shipping_gstin = models.CharField(max_length=50)
    shipping_contact_number = models.CharField(max_length=50)
    shipping_company_name = models.CharField(max_length=50)
    shipping_city = models.CharField(max_length=20)
    shipping_zip_code = models.PositiveIntegerField()
    driver_name = models.CharField(max_length=20, blank=True, default="UNKNOWN")
    driver_number = models.CharField(max_length=50, default="1234567890")
    assigned_vehicle = models.CharField(max_length=10, blank=True, default="UNKNOWN")
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    invoice_date = models.DateTimeField(auto_now_add=True)

    # Other fields in your model

    def __str__(self):
        return self.invoice_id

    def save(self, *args, **kwargs):
        print("enter save fn")
        self.shipping_address = self.shipping_address.capitalize()
        self.shipping_city = self.shipping_city.capitalize()
        self.driver_name = self.driver_name.capitalize()
        self.assigned_vehicle = self.assigned_vehicle.upper()
        if not self.invoice_id:
            current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_id = f"CNS_{current_datetime}"
            self.invoice_id = unique_id
        super().save(*args, **kwargs)


class PaymentModel(models.Model):
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=[('cash', 'cash'), ('online', 'online')])
    payment_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.payment_id)

    # Other fields for your model
    @property
    def created_at_local(self):
        # Convert UTC time to local time
        local_tz = timezone.get_current_timezone()
        return self.created_at.astimezone(local_tz)
