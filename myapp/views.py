from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)  # Corrected to get a single object
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        product = Product.objects.get(pk=pk)  # Corrected typo here
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_permissions(self):
        # AllowAny for 'list' and 'retrieve', IsAuthenticated for 'create', 'update', 'destroy'
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    

class OrderViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)  # Corrected to get a single object
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def create(self, request):
        items_data = request.data.pop('items', [])  # Extract nested items data
        serializer = OrderSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            order = serializer.save()  # User is automatically set via serializer's create()
            
            # Create OrderItems associated with the order
            for item_data in items_data:
                try:
                    product = Product.objects.get(id=item_data['product'])
                    OrderItem.objects.create(order=order, product=product, quantity=item_data['quantity'])
                except KeyError as e:
                    order.delete()  # Rollback if items data is invalid
                    return Response({'error': f'Missing field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
                except Product.DoesNotExist:
                    order.delete()  # Rollback if product doesn't exist
                    return Response({'error': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)

            # Return the created order
            return Response(OrderSerializer(order, context={'request': request}).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get_permissions(self):
        permission_classes = [IsAuthenticated]  # All actions require authentication for Order
        return [permission() for permission in permission_classes]
    

class OrderItemViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = OrderItem.objects.all()
        serializer = OrderItemSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        orderitem = get_object_or_404(OrderItem, pk=pk)  # Corrected to get a single object
        serializer = OrderItemSerializer(orderitem)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get_permissions(self):
        permission_classes = [IsAuthenticated]  # All actions require authentication for OrderItem
        return [permission() for permission in permission_classes]
