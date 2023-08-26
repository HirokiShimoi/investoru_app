from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Product, Inventory, OrderLine

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource


class InventoryResource(resources.ModelResource):
    class Meta:
        model = Inventory

@admin.register(Inventory)
class InventoryAdmin(ImportExportModelAdmin):
    resource_class = InventoryResource

class OrderLineResource(resources.ModelResource):
    class Meta:
        model = OrderLine

@admin.register(OrderLine)
class OrderLineAdmin(ImportExportModelAdmin):
    resource_class = OrderLineResource

