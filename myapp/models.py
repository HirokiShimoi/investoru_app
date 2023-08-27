from django.db import models

class Product(models.Model):
    product_code = models.CharField(max_length=20, unique=True)  # 自社商品コード
    name = models.CharField(max_length=100)  # 商品名
    category = models.CharField(max_length=50)  # カテゴリ
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='product_code')  # 商品ID（外部キー）
    current_stock = models.IntegerField()  # 現在の在庫数

    def __str__(self):
        return f"{self.product.name} - {self.current_stock}"

class OrderLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='product_code')  # 商品ID（外部キー）
    reorder_point = models.IntegerField()  # 発注点

    def __str__(self):
        return f"{self.product.name} - {self.reorder_point}"
