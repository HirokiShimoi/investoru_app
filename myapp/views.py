from django.db.models import F
from rest_framework import status, views,generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Product,Inventory,OrderLine
from .serializers import ProductSerializer, InventorySerializer,OrderLineSerializer,UserSerializer
from django.shortcuts import get_object_or_404,render


class ProductListCreateView(views.APIView):

    def get(self,request):
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
        inventory = get_object_or_404(Inventory, product_code=product_code)
        serializer = InventorySerializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OrderLineListCreateView(views.APIView):

    def get(self,request):
        orderline = OrderLine.objects.all()
        serializer = OrderLineSerializer(orderline, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = OrderLineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderLineDetailView(generics.RetrieveAPIView):
    queryset = OrderLine.objects.all()
    serializer_class = OrderLineSerializer
    lookup_field = 'product_code'


class UnderOrderLine(views.APIView):
    def get(self,request):
        underorderproducts =Inventory.objects.annotate(
            reorder_point = F('product__orderline__reorder_point')
        ).filter(current_stock__lte=F('reorder_point'))

        print("Under Order Products: ", underorderproducts.query)

        serializer = InventorySerializer(underorderproducts, many=True)
        return Response(serializer.data)
    
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

