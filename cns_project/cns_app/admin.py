from django.contrib import admin
from .models import RawMaterialModel, ProductionModel, InvoiceModel, Customer, User, UserProfile, PaymentModel, RawExpenseModel
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateTimeWidget
from .models import RawMaterialModel
from datetime import datetime

class RawMaterialResource(resources.ModelResource):
    created_at = Field(attribute='created_at', column_name='created_at', widget=DateTimeWidget(format='%Y-%m-%d %H:%M:%S'))
    updated_at = Field(attribute='updated_at', column_name='updated_at', widget=DateTimeWidget(format='%Y-%m-%d %H:%M:%S'))

    class Meta:
        model = RawMaterialModel
        import_id_fields = ('rst_no',)  # Use rst_no as the unique identifier for imports

    def before_import_row(self, row, **kwargs):
        # Convert the date string to a datetime object
        if 'created_at' in row:
            row['created_at'] = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
    def before_save(self, obj, **kwargs):
        # Set created_at and updated_at if they are provided in the import
        if 'created_at' in kwargs:
            obj.created_at = kwargs['created_at']
            print(f"Setting created_at to: {obj.created_at}")
        if 'updated_at' in kwargs:
            obj.updated_at = kwargs['updated_at']
            print(f"Setting updated_at to: {obj.updated_at}")



# Register your models here.
# admin.site.register(RawMaterialModel, ImportExportModelAdmin)
admin.site.register(ProductionModel, ImportExportModelAdmin)
admin.site.register(InvoiceModel, ImportExportModelAdmin)
admin.site.register(Customer, ImportExportModelAdmin)
admin.site.register(PaymentModel, ImportExportModelAdmin)
admin.site.register(RawExpenseModel, ImportExportModelAdmin)

@admin.register(RawMaterialModel)
class RawMaterialAdmin(ImportExportModelAdmin):
    resource_class = RawMaterialResource