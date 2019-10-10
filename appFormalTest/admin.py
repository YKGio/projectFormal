from django.contrib import admin
from .models import Customers, Stock, Employee, CombineStock, Sale, SetSale, CusOwnSet, Shop, InStock, importReport, Commission, CommLimit, MultiSevicePercent, RegularBonus, SalarySelectEmp
from import_export import resources
from import_export.admin import ImportExportModelAdmin



class CustomersResource(resources.ModelResource):

    class Meta:
        model = Customers
        #exclude = ('cusBirthDate')
        #import_id_fields = ('cusCode',)

class CustomersAdmin(ImportExportModelAdmin):
    list_display = (
        'cusName','cusCode','cusPhoneNum',
        'cusSex','cusRemarks')
    resource_class = CustomersResource
    #to_encoding = 'utf-8'

admin.site.register(Customers, CustomersAdmin)
admin.site.register(Stock)
admin.site.register(Employee)
admin.site.register(CombineStock)
admin.site.register(Sale)
admin.site.register(SetSale)
admin.site.register(CusOwnSet)
admin.site.register(Shop)
admin.site.register(InStock)
admin.site.register(importReport)
admin.site.register(Commission)
admin.site.register(CommLimit)
admin.site.register(MultiSevicePercent)
admin.site.register(RegularBonus)
admin.site.register(SalarySelectEmp)
