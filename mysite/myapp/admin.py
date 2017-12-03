from django.contrib import admin
from .models import Product, Review, Voucher

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sku', 'photo','press', 'created_at')
    list_filter = ('name','sku',)
    search_fields = ('name',)
    ordering = ('id',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Voucher)
