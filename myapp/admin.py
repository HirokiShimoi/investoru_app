from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Product, Inventory, OrderLine
from import_export import fields
from import_export.widgets import ForeignKeyWidget


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        import_id_fields = ['product_code']
        
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    import_export_options = {'update': True}


class InventoryResource(resources.ModelResource):
    product = fields.Field(
        column_name='product_code',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'product_code')
    )

    class Meta:
        model = Inventory
        fields = ('id', 'product', 'current_stock')

@admin.register(Inventory)
class InventoryAdmin(ImportExportModelAdmin):
    resource_class = InventoryResource

class OrderLineResource(resources.ModelResource):
    product = fields.Field(
        column_name='product_code',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'product_code')
    )

    class Meta:
        model = OrderLine
        fields = ('id', 'product', 'reorder_point')

@admin.register(OrderLine)
class OrderLineAdmin(ImportExportModelAdmin):
    resource_class = OrderLineResource

