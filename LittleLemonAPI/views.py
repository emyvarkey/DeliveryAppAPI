from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from .models import MenuItem,Category
from django.contrib.auth.models import User, Group
from .serializer import MenuItemSerializer ,CategorySerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsManagerOrSuperUser,IsDeliveryCrewOrSuperUser
from rest_framework import status

# Create your views here.

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemView (viewsets.ModelViewSet):

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes =[]
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsManagerOrSuperUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    ordering_fields = ['price']
    filterset_fields = ['price','featured','category']
    search_fields = ['title','category__tittle']
    
    
'''  
    def update(self, request, pk=None):
        return Response({"message":"Updating menu item with id: "+str(pk)}, status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
     return Response({"message":"Displaying menu item with id: "+str(pk)}, status.HTTP_200_OK)
    def partial_update(self, request, pk=None):
        return Response({"message":"Partially updating a menu item with id: "+str(pk)}, status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        return Response({"message":"Deleting menu item with id: "+str(pk)}, status.HTTP_200_OK)
''' 

class ManagerGroupView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManagerOrSuperUser]

    def get_queryset(self):
        return User.objects.filter(groups__name='Manager')
    
    def create(self, request):

        # Custom behavior for POST request
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

            manager_group, _ = Group.objects.get_or_create(name='Manager')
            manager_group.user_set.add(user)


        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    
class DeleteManagerView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManagerOrSuperUser]
    def delete(self, request, pk):

        try:
            user = User.objects.get(id = pk)
            if user.groups.filter(name='Manager').exists():
                user.delete() 
                return Response({"detail": "200 – Success"},status=status.HTTP_200_OK)
            else:
                return Response ({"detail": "User is not a manager"},status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

class DeliveryCrewGroupView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManagerOrSuperUser]

    def get_queryset(self):
        return User.objects.filter(groups__name='Delivery crew')
    
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

            delivery_group, _ = Group.objects.get_or_create(name='Delivery crew')
            delivery_group.user_set.add(user)


        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
class DeleteDeliveryCrewView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name='Delivery crew')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManagerOrSuperUser]
    def delete(self, request, pk):
        try:
            user = User.objects.get(id = pk)
            if user.groups.filter(name='Delivery crew').exists():
                user.delete() 
                return Response({"detail": "200 – Success"},status=status.HTTP_200_OK)
            else:
                return Response ({"detail": "User is not a delivery crew member"},status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)