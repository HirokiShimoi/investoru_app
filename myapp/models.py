from django.db import models
from django.contrib.auth.models import AbstractUser

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
    product = models.OneToOneField(Product, on_delete=models.CASCADE, to_field='product_code')  # 商品ID（外部キー）
    reorder_point = models.IntegerField()  # 発注点

    def __str__(self):
        return f"{self.product.name} - {self.reorder_point}"

class SelectedItem(models.Model):
    category = models.CharField(max_length=50)
    inventory = models.IntegerField()
    orderpoint = models.IntegerField()
    product_code = models.CharField(max_length=20)
    product_name = models.CharField(max_length=100)

    def __str__(self):
        return self.product_name

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='product_code')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.text[:20]}"


class Todo(models.Model):
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        status = "Completed" if self.is_completed else "Incomplete"
        due_date_str = self.due_date.strftime('%Y-%m-%d') if self.due_date else "No due date"
        return f"{self.text[:20]} ({status}, Due: {due_date_str})"