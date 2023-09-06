from django.db.models import F,Q
from rest_framework import status, views,generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Product,Inventory,OrderLine,SelectedItem
from .serializers import ProductSerializer, InventorySerializer,OrderLineSerializer,UserSerializer,SelectedItemSerializer
from django.shortcuts import get_object_or_404,render
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ProductListCreateView(views.APIView):

    def get(self, request):
        category = request.GET.get('category',None)

        if category:
            products = Product.objects.filter(category=category)
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'product_code'
    

class InventoryListCreateView(views.APIView):

    def get(self,request):
        inventory = Inventory.objects.all()
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class InventoryDetailView(generics.RetrieveAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    lookup_field = 'product_code'

class InventoryUpdateView(views.APIView):
    def put(self,request,product_code):
        print(f"Product code received: {product_code}")
        print(f"Request data received: {request.data}")
        inventory = get_object_or_404(Inventory, product_code=product_code)
        print(f"inventory data received: {inventory}")
        serializer = InventorySerializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OrderLineListCreateView(views.APIView):

    def get(self,request):
        paginator = CustomPageNumberPagination()

        category = request.GET.get('category',None)
        basequery = OrderLine.objects.annotate(
            reorder_point = F('product__reorder_point')
        ).filter(current_stock__lte=F('reorder_point'))

        if category:
            filtered_query = basequery.filter(product__category=category)
        else:
            filtered_query = basequery

        result_page = paginator.paginate_queryset(filtered_query, request)
        serializer = OrderLineSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self,request):
        serializer = OrderLineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,product_code):
        orderline = get_object_or_404(OrderLine, product__product_code = product_code)
        print(f"Product code received: {orderline}")
        serializer = OrderLineSerializer(orderline, data=request.data,  partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderLineDetailView(generics.RetrieveAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer
    lookup_field = 'product_code'


class UnderOrderLine(views.APIView):
    def get(self, request):
        paginator = CustomPageNumberPagination()
        
        category = request.GET.get('category', None)
        base_query = Inventory.objects.annotate(
            annotation_reorder_point=F('product__orderline__reorder_point')
        ).filter(current_stock__lte=F('annotation_reorder_point'),product__is_active=True)
        
        if category:
            filtered_query = base_query.filter(product__category=category)
        else:
            filtered_query = base_query

        result_page = paginator.paginate_queryset(filtered_query, request)
        serializer = InventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class UserCreateView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class SelectedItemView(generics.CreateAPIView):
    queryset = SelectedItem.objects.all()
    serializer_class = SelectedItemSerializer