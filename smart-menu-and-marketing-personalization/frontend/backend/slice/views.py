from random import randint
from django.utils import timezone
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from .permissions import IsAdminOrReadOnly, IsOwner, IsAdmin

# ----------------------------
# USERS
# ----------------------------

class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.validated_data['is_active'] = True
        user = serializer.save()
        user.set_password(user.password)
        user.save()

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin | IsOwner]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class UserMeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsOwner]
    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

# ----------------------------
# ADMINS
# ----------------------------

class CreateAdminView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        serializer.validated_data['is_active'] = True
        serializer.validated_data['role'] = User.Role.ADMIN
        user = serializer.save()
        user.set_password(user.password)
        user.save()

class MakeAdminView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def perform_update(self, serializer):
        serializer.validated_data['role'] = User.Role.ADMIN
        serializer.save()

# ----------------------------
# STORES
# ----------------------------

class StoreListCreateView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAdminOrReadOnly]

class StoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAdminOrReadOnly]

# ----------------------------
# STOCK ITEMS
# ----------------------------

class StockItemListCreateView(generics.ListCreateAPIView):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer
    permission_classes = [IsAdmin]

class StockItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer
    permission_classes = [IsAdmin]

# ----------------------------
# MENUS
# ----------------------------

class MenuListCreateView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdmin]

class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdmin]

# ----------------------------
# MENU ITEMS
# ----------------------------

class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

# ----------------------------
# ORDERS
# ----------------------------

class OrderListCreateView(generics.CreateAPIView):
    queryset = Order.objects.none()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.validated_data['display_id'] = f"ORD-{randint(1000,9999)}"
        serializer.validated_data['created_at'] = timezone.now()
        serializer.validated_data['status'] = Order.Status.PENDING
        serializer.validated_data['total'] = sum([item['price'] * item['qty'] for item in serializer.validated_data['items']])
        serializer.save()

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdmin | IsOwner]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return Order.objects.all()
        return Order.objects.filter(user=user).order_by('-created_at')

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdmin | IsOwner]

    def perform_update(self, serializer):
        old_instance = self.get_object()
        user = serializer.validated_data.get('user', self.get_object().user)
        new_items = serializer.validated_data.get('items', old_instance.items or [])
        total = serializer.validated_data['total'] = sum([item['price'] * item['qty'] for item in new_items])
        # Check status transitions
        match old_instance.status and user.role=='USER':
            case Order.Status.CONFIRMED:
                raise serializers.ValidationError("Cannot modify a confirmed order, please cancel before the preparation phase.")
            case Order.Status.CANCELLED:
                raise serializers.ValidationError("Cannot modify a cancelled order.")
            case Order.Status.COMPLETED:
                raise serializers.ValidationError("Cannot modify a completed order.")
            case Order.Status.PREPARING if serializer.validated_data.get('status') != Order.Status.CANCELLED:
                raise serializers.ValidationError("Cannot modify an order in preparation.")
        
        # Only update user's XP and nexo coins if order status is being set to CONFIRMED
        new_status = serializer.validated_data.get('status', old_instance.status)
        if new_status == Order.Status.COMPLETED:
            new_items = serializer.validated_data.get('items', old_instance.items)
            itemcount = sum([item['qty'] for item in new_items])
            user.xp += itemcount * 10  # 10 XP per item
            user.nexo_coins += total * 0.3  # 30% of the total in nexo coins
            while user.xp >= 100:  # level up for every 100 XP
                user.level += 1
                user.xp -= 100
            user.save()

        serializer.save()
 
    def perform_destroy(self, instance):
        if instance.status in [Order.Status.COMPLETED, Order.Status.CANCELLED, Order.Status.PREPARING]:
            raise serializers.ValidationError("Cannot cancel a completed, in preparation or already cancelled order.")
        instance.status = Order.Status.CANCELLED
        instance.save()