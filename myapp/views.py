from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response
from .models import Product,Inventory,OrderLine
from .serializers import ProductSerializer, InventorySerializer,OrderLineSerializer

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
