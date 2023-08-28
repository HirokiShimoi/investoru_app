from django.urls import path
from . import views  # ここでviews.pyをインポート

urlpatterns = [
    path('api/products/', views.ProductListCreateView.as_view(), name='product-list-create'),
]
