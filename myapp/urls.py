from django.urls import path
from . import views  # ここでviews.pyをインポート

urlpatterns = [
    path('api/inventory/reorder/', views.UnderOrderLine.as_view(), name='under-order-products'), #カテゴリ別の発注点より少ない在庫アイテム一覧（ページネーション済み）
    path('api/products/', views.ProductListCreateView.as_view(), name='product-list-create'), #全商品一覧
    path('api/inventory/', views.InventoryListCreateView.as_view(), name='inventory-list-create'),#在庫と自社コード一覧
    path('api/orderline/<str:product_code>/', views.OrderLineListCreateView.as_view(), name='orderline-list-create'),
    path('api/products/<str:product_code>/', views.ProductDetailView.as_view(), name='product-detail'),#自社コードでソートしたアイテム
    path('api/inventory/<str:product_code>/', views.InventoryDetailView.as_view(), name='inventory-detail'),#自社コードでソートした在庫アイテム
    #path('api/orderline/<str:product_code>/', views.OrderLineDetailView.as_view(), name='orderline-detail'),
    path('api/inventory/update/<str:product_code>/', views.InventoryUpdateView.as_view(), name='inventory-update'),
    path('api/create_user/', views.UserCreateView.as_view(),name = 'user-create'),
    path('api/selecteditem/', views.SelectedItemView.as_view(), name='selecteditem-create'),#チェック入った商品
    path('api/comment/', views.CommentView.as_view(), name='comment'),#チェック入った商品
    path('api/todo/',views.TodoView.as_view(), name='todo'),
]
