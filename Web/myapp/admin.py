from django.contrib import admin
from .models import *


admin.site.site_header = 'Admin'
admin.site.index_title = 'Main Admin'
admin.site.site_title = 'Backend'

class AllproductAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'instock', 'price', 'quantity']
	list_editable = ['price', 'instock', 'quantity']

admin.site.register(Allproduct, AllproductAdmin)
admin.site.register(Profile)
admin.site.register(Cart)

class OrderListAdmin(admin.ModelAdmin):
	list_display = ['orderid', 'productname', 'total']

admin.site.register(OrderList, OrderListAdmin)
admin.site.register(OrderPending)

