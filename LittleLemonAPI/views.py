from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from .models import MenuItem,Category,Cart,Order,OrderItem
from django.contrib.auth.models import User, Group
from .serializers import MenuItemSerializer ,CategorySerializer, UserSerializer,CartSerializer,OrderSerializer,OrderItemSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,BasePermission
from rest_framework.decorators import permission_classes
from .permissions import IsManager,IsDeliveryCrew,IsCustomer
from rest_framework import status
from datetime import datetime
from decimal import Decimal
from rest_framework.exceptions import ValidationError
import logging

from django.db import transaction

logger = logging.getLogger('views')

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.groups.filter(name='Manager').exists())
    group_name = 'Manager'


# Create your views here.

class CategoriesView(viewsets.ModelViewSet):
    def get_permissions(self):
        permission_classes =[]
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsManagerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    ordering_fields = ['title']
    filterset_fields = ['title']
    search_fields = ['tittle']

class MenuItemView (viewsets.ModelViewSet):

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes =[]
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsManagerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    ordering_fields = ['price']
    filterset_fields = ['price','featured','category__title']
    search_fields = ['title','category__tittle']
       
class ManagerGroupManagementViewSet(viewsets.ViewSet):

    search_fields = ['username']

    def get_permissions(self):
        permission_classes =[IsAuthenticated,IsManagerOrAdmin]
        return [permission() for permission in permission_classes]
    

    def list(self, request):
        queryset = User.objects.filter(groups__name='Manager')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            if email:
                user.email = email
            user.save()

            group, _ = Group.objects.get_or_create(name='Manager')
            group.user_set.add(user)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        manager_group = Group.objects.get(name='Manager')
        if manager_group in user.groups.all():
            user.groups.remove(manager_group)
            return Response({"success": "User removed from Manager group"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not in the Manager group"}, status=status.HTTP_400_BAD_REQUEST)
        
class DeliveryCrewGroupManagementViewSet(viewsets.ViewSet):

    search_fields = ['username']


    def get_permissions(self):
        permission_classes =[IsAuthenticated,IsManager]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = User.objects.filter(groups__name='Delivery crew')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            if email:
                user.email = email
            user.save()

            group, _ = Group.objects.get_or_create(name='Delivery crew')
            group.user_set.add(user)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        delivery_crew_group = Group.objects.get(name='Delivery crew')
        if delivery_crew_group in user.groups.all():
            user.groups.remove(delivery_crew_group)
            return Response({"success": "User removed from Delivery group"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not in the Delivery group"}, status=status.HTTP_400_BAD_REQUEST)
 

#Cart management endpoints 

class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        logger.debug(f"Fetching the cart for user: {user}")
        return Cart.objects.filter(user = user)

    def perform_create(self, serializer):
        user = self.request.user
        logger.debug(f"Creating the cart for user: {user}")
        menuitem_id = self.request.data.get('menuitem_id')
        quantity = self.request.data.get('quantity')
        
        try:
            menuitem = MenuItem.objects.get(id=menuitem_id)
            logger.debug(f"Fetching the menuitem with id {menuitem_id} for user: {user}")
        except MenuItem.DoesNotExist:
            logger.debug(f"Menu item not found: {menuitem_id}")
            return Response({"error": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        unit_price = menuitem.price
        quantity = int(quantity)
        price = quantity * unit_price

        try:
            existing_cart_item = Cart.objects.get(user=user, menuitem=menuitem.id)
            logger.debug(f"Found existing cart item for user {user} and menuitem {menuitem_id}: {existing_cart_item}")
            existing_cart_item.quantity += quantity
            logger.debug(f"Cart item for user {user} and menuitem {menuitem_id} , quantity is updated to {existing_cart_item.quantity}.")
            existing_cart_item.price += price
            logger.debug(f"Cart item for user {user} and menuitem {menuitem_id} , price is updated to {existing_cart_item.price}.")
            existing_cart_item.save()
            serializer = CartSerializer(existing_cart_item)
        except Cart.DoesNotExist:
            logger.debug(f"Cart item for user {user} and menuitem {menuitem_id} not found, creating new cart item.")
            cart_item = serializer.save(user=user, menuitem=menuitem, unit_price=unit_price, price=price)
            # Create a new serializer instance with the new cart item
            serializer = CartSerializer(cart_item)
            logger.debug(f"New cart item created for user {user} and menuitem {menuitem_id}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = self.request.user
        Cart.objects.filter(user=user).delete()
        logger.debug(f"Cart for user {user} has been deleted")
        return Response({"detail": "Your cart has been deleted."}, status=status.HTTP_200_OK)

# Order management endpoints

class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists() :
            return Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            logger.error("No items in the cart for user: %s", user)
            raise ValidationError("No items in the cart")

        logger.debug("Creating order for user: %s", user)
        total = self.calculate_total(cart_items)
        date = datetime.now().date()

        order = serializer.save(user=user, total=total, date=date)
        logger.debug("Order created with ID: %s", order.id)

        for cart_item in cart_items:
            try:
                logger.debug(f"Creating order item for cart: {cart_item.id}")
                logger.debug(f"Cart Details order: {order} are/n menuitem = {cart_item.menuitem}, quantity = {cart_item.quantity}, unit_price = {cart_item.unit_price}, price = {cart_item.price}")

                OrderItem.objects.create(
                    order=order,
                    menuitem=cart_item.menuitem,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.unit_price,
                    price=cart_item.price
                )
                cart_item.delete()
                logger.debug(f"Created order item for menuitem ID: {cart_item.menuitem.id}")
            except Exception as e:
                logger.error(f"Failed to create order item for cart {cart_item.id}: because of {e}")
                raise ValidationError(f"Failed to create order item for menuitem ID {cart_item.menuitem.id}: {e}")

        logger.debug("Order items created for order ID: %s", order.id)
        if Cart.objects.filter(user=user).exists():
            logger.debug("Cart items deleted for user: %s", user)

    def calculate_total(self, cart_items):
        total = Decimal('0.00')
        for cart_item in cart_items:
            total += cart_item.price
        return total

    def partial_update(self, request, pk=None):

        user = self.request.user
        is_deliverycrew = user.groups.filter(name='Delivery crew').exists()
        is_manager = user.groups.filter(name='Manager').exists()
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        if is_deliverycrew and order.user == user:
            try:
                status_value = request.data.get('status')
                order.status = bool(int(status_value))
                order.save()
                logger.debug(f"Order {pk} status updated to {order.status} by delivery crew user {user}")
                return Response({"detail": "Order status updated"}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Failed to update order {pk} status: {e}")
                return Response({"detail": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
            
        elif is_manager:
            try:
                if 'delivery_crew_id' in request.data:
                    delivery_crew_id = request.data.get('delivery_crew_id')
                    order.delivery_crew = User.objects.get(id = delivery_crew_id)
                    logger.debug(f"Order {pk} delivery crew updated to {order.delivery_crew} by manager {user}")
                    order.save()
                    return Response({"success": "Delivery crew updated successfully"}, status=status.HTTP_200_OK)
                elif 'status' in request.data:
                    status_value = request.data.get('status')
                    order.status = bool(int(status_value))
                    order.save()
                    logger.debug(f"Order {pk} status updated to {order.status} by delivery crew user {user}")
                    return Response({"detail": "Order status updated"}, status=status.HTTP_200_OK)
                else:
                    return Response({"success": "Delivery crew updated successfully"}, status=status.HTTP_200_OK)

                

            except User.DoesNotExist:
                # Logging failure to find delivery crew user
                logger.error(f"Delivery crew user with id {delivery_crew_id} not found")
                return Response({"detail": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Logging general failure to update delivery crew
                logger.error(f"Failed to update delivery crew for order {pk}: {e}")
                return Response({"detail": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # Logging unauthorized access attempt
            logger.error(f"User {user} does not have permission to update order {pk}")
            return Response({"error": "You do not have permission to update this order"}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        user = request.user
        is_manager = user.groups.filter(name='Manager').exists()
        if is_manager:
            try:
                order = Order.objects.get(pk=pk)
                order.delete()
                # Logging order deletion
                logger.debug(f"Order {pk} deleted by manager {user}")
                return Response({"detail": f"Order item with id = {pk} has been deleted."}, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                logger.error(f"Order {pk} not found for deletion")
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND) 
        else:
            logger.error(f"User {user} does not have permission to delete order {pk}")
            return Response({"error": "You do not have permission to delete this order"}, status=status.HTTP_403_FORBIDDEN)
