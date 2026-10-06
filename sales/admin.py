from django.contrib import admin
from .models import Product, Shop, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=("name","price","stock","active")
    search_fields=("name",)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display=("name","owner_name","phone","created_at")
    search_fields=("name","owner_name","phone")

class OrderItemInline(admin.TabularInline):
    model=OrderItem
    extra=0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=("id","shop","salesman","total_amount","paid_amount","payment_method","order_date")
    list_filter=("payment_method","order_date")
    inlines=[OrderItemInline]
