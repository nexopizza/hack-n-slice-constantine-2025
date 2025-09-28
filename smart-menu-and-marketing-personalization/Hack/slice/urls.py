from django.contrib import admin
from django.urls import path
from slice.views import *
urlpatterns = [
    # Users
    path('users/add/', UserView.as_view(), name='user-create'),
    path('users/me/', UserMeView.as_view(), name='user-me'),

    # Admins
    path('admins/add/', CreateAdminView.as_view(), name='admin-create'),
    path('admins/<int:pk>/', UserDetailView.as_view(), name='admin-detail'),
    path('admins/list/', UserListView.as_view(), name='admin-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/list/', UserListView.as_view(), name='user-list'),

    # Stores
    path("stores/", StoreListCreateView.as_view(), name="store-list"),
    path("stores/<uuid:pk>/", StoreDetailView.as_view(), name="store-detail"),

    # Stock Items
    path("stock-items/", StockItemListCreateView.as_view(), name="stockitem-list"),
    path("stock-items/<str:pk>/", StockItemDetailView.as_view(), name="stockitem-detail"),

    # Menus
    path("menus/", MenuListCreateView.as_view(), name="menu-list"),
    path("menus/<str:pk>/", MenuDetailView.as_view(), name="menu-detail"),

    # Menu Items
    path("menu-items/", MenuItemListCreateView.as_view(), name="menuitem-list"),
    path("menu-items/<int:pk>/", MenuItemDetailView.as_view(), name="menuitem-detail"),

    # Orders
    path("orders/", OrderListView.as_view(), name="order-list-user"),
    path("orders/add/", OrderListCreateView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]