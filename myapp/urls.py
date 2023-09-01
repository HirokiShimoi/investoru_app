from django.urls import path
from . import views  

urlpatterns = [
    path('api/inventory/reorder/', views.UnderOrderLine.as_view(), name='under-order-products'),
    path('api/products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('api/inventory/', views.InventoryListCreateView.as_view(), name='inventory-list-create'),
    path('api/orderline/', views.OrderLineListCreateView.as_view(), name='orderline-list-create'),
    path('api/products/<str:product_code>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('api/inventory/<str:product_code>/', views.ProductDetailView.as_view(), name='inventory-detail'),
    path('api/orderline/<str:product_code>/', views.ProductDetailView.as_view(), name='orderline-detail'),
    path('api/inventory/update/<str:product_code>/', views.InventoryUpdateView.as_view(), name='inventory-update'),
    path('api/create_user/',views.UserCreateView.as_view(),name = 'user-create'),
    
]
