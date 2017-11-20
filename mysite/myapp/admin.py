from django.contrib import admin
from .models import Product, Review

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=('id', 'name', 'sku', 'photo',)
    list_filter=('name','sku',)
    search_fields=('name',)
    ordering=('id',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
