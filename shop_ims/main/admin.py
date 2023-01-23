from django.contrib import admin
from . import models
# Register your mfodels here.

admin.site.register(models.Unit)
admin.site.register(models.Vendor )

class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['customer_name', 'customer_mobile' ]
    search_fields = ['customer_name', 'customer_mobile',  ]
admin.site.register(models.Customer, CustomerAdmin  )


class ProductAdmin(admin.ModelAdmin):
      search_fields = ['title', 'unit__title'  ]  
      list_display = ['title', 'unit' ]

admin.site.register(models.Product, ProductAdmin )

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendor', 'product', 'quantity', 'price','total_amount', 'vendor','purchace_date' ]



admin.site.register(models.Purchase, PurchaseAdmin  )

class SaleAdmin(admin.ModelAdmin):
   
    list_display = [
        'id',
        'customer',
        'product',
         'quantity',
          'price', 
          'total_amount',
'sales_date',

   ]


admin.site.register(models.Sale, SaleAdmin)



class InventoryAdmin(admin.ModelAdmin):
  search_fields = ['product__title', 'product__unit__title' ]  
  list_display = [
    'id',
    'product',

'purchase_quantity',

'sales_quantity',
'total_balance_quantity',
'product_unit',
'purchase_date',
'sale_date',


 ]

admin.site.register(models.Inventory, InventoryAdmin )



