from django.contrib import admin
from .models import UserProfile,Category,Product,Business,Receipt,ReceiptItems


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','phone_number','profile_image','national_id')

class CategoryAdmin(admin.ModelAdmin):
    list_display=("name",)

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','get_item_profit','product_category','product_code','unit_price','purchase_date','end_on','expires_on','total_inital_units','business','available_units','sold_unit','damaged_units')

class BusinessAdmin(admin.ModelAdmin):
    list_display=('name','get_products','county','owner','city','street',)

class ReceiptAdmin(admin.ModelAdmin):
    list_display=('receipt_items','total_amount','sold_at','business')

class ReceiptItemsAdmin(admin.ModelAdmin):
    list_display = ('product','selling_price_per_unit','units','items_return')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Business,BusinessAdmin)
admin.site.register(Receipt,ReceiptAdmin)
admin.site.register(ReceiptItems,ReceiptItemsAdmin)