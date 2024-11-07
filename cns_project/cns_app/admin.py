from django.contrib import admin
from .models import RawMaterialModel, ProductionModel, InvoiceModel, Customer, User, UserProfile, PaymentModel, RawExpenseModel
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(RawMaterialModel, ImportExportModelAdmin)
admin.site.register(ProductionModel, ImportExportModelAdmin)
admin.site.register(InvoiceModel, ImportExportModelAdmin)
admin.site.register(Customer, ImportExportModelAdmin)
admin.site.register(PaymentModel, ImportExportModelAdmin)
admin.site.register(RawExpenseModel, ImportExportModelAdmin)

