from django.db.models import F,Q
from rest_framework import status, views,generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Product,Inventory,OrderLine,SelectedItem,Comment,Todo
from .serializers import ProductSerializer, InventorySerializer,OrderLineSerializer,UserSerializer,SelectedItemSerializer,CommentSerializer,TodoSerializer
from django.shortcuts import get_object_or_404,render
from rest_framework.pagination import PageNumberPagination
import csv
from io import TextIOWrapper
from django.http import JsonResponse


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        category = request.GET.get('category',None)
        product_code = request.GET.get('product_code',None)
        keyword = request.GET.get('keyword', None)

        queryset = Product.objects.all()

        if category:
            queryset = queryset.filter(category=category)

        if product_code:
            queryset = queryset.filter(product_code=product_code)

        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword))

        serializer = ProductSerializer(queryset, many=True)
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

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = SelectedItemSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        try:
            delete_items = request.data.get('ids',[])
            print("delete_items:", delete_items)
            SelectedItem.objects.filter(product_code__in = delete_items).delete()
            return Response ({'status': 'items deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CommentView(views.APIView):
    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoView(views.APIView):
    def get(self, request, format=None):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos,many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailView(views.APIView):    
    def put(self,request,pk,format=None):
        todo = get_object_or_404(Todo, pk=pk)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UpdateInventoryCSV(views.APIView):
    def put(self,request):
        try:
            csv_file = request.FILES['file']
            csv_file = TextIOWrapper(csv_file.file, encoding='utf-8')
            csv_reader = csv.reader(csv_file)

            updated_inventories = []
            created_products = []
            print("Reading CSV file")
            for row in csv_reader:
                print(f"Processing row: {row}")
                product_code = row[2]
                product_name = row[3]
                current_stock = int(row[11])

                product, created = Product.objects.get_or_create(
                    product_code=product_code,
                    defaults={'name': product_name}
                )

                if created:
                    created_products.append(product)

                inventory, _ = Inventory.objects.get_or_create(
                    product=product,
                    defaults={'current_stock': current_stock}
                )
                inventory.current_stock = current_stock
                updated_inventories.append(inventory) 
                print("CSV file received:", csv_file)
                print("Created products:", created_products)
                print("Updated inventories:", updated_inventories)

            if created_products:
                Product.objects.bulk_create(created_products)

            if updated_inventories:
                Inventory.objects.bulk_update(updated_inventories, ['current_stock'])
        
            return JsonResponse({'status': 'success', 'message': 'CSV uploaded and inventory updated.'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})