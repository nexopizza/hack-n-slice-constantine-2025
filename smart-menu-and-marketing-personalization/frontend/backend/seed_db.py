# seed_db.py
import os
import django
from django.core.files import File
from datetime import time, timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hack.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from slice.models import User, Store, StockItem, Menu, MenuItem, Order
import random
import json
from decimal import Decimal

class DatabaseSeeder:
    def __init__(self):
        self.users = []
        self.stores = []
        self.stock_items = []
        self.menus = []
        self.menu_items = []
        self.orders = []

    def clear_database(self):
        """Clear existing data"""
        print("Clearing existing data...")
        Order.objects.all().delete()
        MenuItem.objects.all().delete()
        Menu.objects.all().delete()
        StockItem.objects.all().delete()
        Store.objects.all().delete()
        User.objects.all().delete()

    def create_users(self):
        """Create sample users with Algerian names"""
        print("Creating users...")

        users_data = [
            {
            'username': 'karim_dz', 'email': 'karim@example.dz',
            'first_name': 'Karim', 'last_name': 'Bensaïd',
            'phone': '+213551234568', 'address': '456 Rue Hassiba Ben Bouali',
            'city': 'Alger', 'role': 'ADMIN',
            'nexo_coins': 250, 'xp': 1200, 'level': 3,
            'prefs': {"cuisine": ["Italienne"], "diet": "Aucun", "favorites": []}
        },
        {
            'username': 'amina_dz', 'email': 'amina@example.dz',
            'first_name': 'Amina', 'last_name': 'Zerrouki',
            'phone': '+213551234569', 'address': '789 Avenue des Frères Oudek',
            'city': 'Oran', 'role': 'USER',
            'nexo_coins': 500, 'xp': 800, 'level': 2,
            'prefs': {"cuisine": ["Végétarienne"], "diet": "Végétarien", "favorites": []}
        },
        {
            'username': 'yacine_dz', 'email': 'yacine@example.dz',
            'first_name': 'Yacine', 'last_name': 'Kadri',
            'phone': '+213551234570', 'address': '321 Rue Abane Ramdane',
            'city': 'Constantine', 'role': 'USER',
            'nexo_coins': 150, 'xp': 300, 'level': 1,
            'prefs': {"cuisine": ["Italienne", "Algérienne"], "diet": "Aucun", "favorites": []}
        },
        {
            'username': 'test', 'email': 'test@example.dz',
            'first_name': 'test', 'last_name': 'test',
            'phone': '+213123456789', 'address': '123 Rue Hassiba Ben Bouali',
            'city': 'Alger', 'role': 'ADMIN',
            'nexo_coins': 250, 'xp': 1200, 'level': 3,
            'prefs': {"cuisine": ["Italienne"], "diet": "Aucun", "favorites": []}
        },
    ]

        for user_data in users_data:
            if user_data['role'] == 'ADMIN':
                user = User.objects.create_superuser(
                username=user_data['username'],
                email=user_data['email'],
                password="password123",
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data['phone'],
                address=user_data['address'],
                city=user_data['city'],
                nexo_coins=user_data['nexo_coins'],
                xp=user_data['xp'],
                level=user_data['level'],
                prefs=user_data['prefs'],
            )
            else:
                user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password="password123",
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data['phone'],
                address=user_data['address'],
                city=user_data['city'],
                nexo_coins=user_data['nexo_coins'],
                xp=user_data['xp'],
                level=user_data['level'],
                prefs=user_data['prefs'],
            )
            self.users.append(user)

    def create_stores(self):
        """Create sample stores in Algerian cities"""
        print("Creating stores...")
        
        stores_data = [
            {
                'name': 'Nexo Pizza Alger Centre', 
                'city': 'Alger', 
                'country': 'Algérie',
                'timezone': 'Africa/Algiers',
                'open_at': time(10, 0),
                'close_at': time(23, 0),
                'capacity': 50,
                'features': ["delivery", "takeaway", "kds"]
            },
            {
                'name': 'Nexo Pizza Oran', 
                'city': 'Oran', 
                'country': 'Algérie',
                'timezone': 'Africa/Algiers',
                'open_at': time(11, 0),
                'close_at': time(22, 0),
                'capacity': 30,
                'features': ["delivery", "takeaway"]
            },
            {
                'name': 'Nexo Pizza Constantine', 
                'city': 'Constantine', 
                'country': 'Algérie',
                'timezone': 'Africa/Algiers',
                'open_at': time(10, 30),
                'close_at': time(22, 30),
                'capacity': 40,
                'features': ["delivery", "takeaway", "kds", "dinein"]
            }
        ]

        for store_data in stores_data:
            store = Store.objects.create(**store_data)
            self.stores.append(store)

    def create_stock_items(self):
        """Create stock items for all ingredients"""
        print("Creating stock items...")
        
        stock_data = [
            # Dough
            {'stock_item_id': 'DOUGH001', 'name': 'Pâte à Pizza Classique', 'category': StockItem.Category.DOUGH, 'unit': 'kg', 'par_level': 50.0, 'price_per_unit': 250.00},
            {'stock_item_id': 'DOUGH002', 'name': 'Pâte Complète', 'category': StockItem.Category.DOUGH, 'unit': 'kg', 'par_level': 20.0, 'price_per_unit': 300.00},
            
            # Cheese
            {'stock_item_id': 'CHEESE001', 'name': 'Mozzarella', 'category': StockItem.Category.CHEESE, 'unit': 'kg', 'par_level': 30.0, 'price_per_unit': 800.00},
            {'stock_item_id': 'CHEESE002', 'name': 'Cheddar', 'category': StockItem.Category.CHEESE, 'unit': 'kg', 'par_level': 10.0, 'price_per_unit': 900.00},
            {'stock_item_id': 'CHEESE003', 'name': 'Gruyère', 'category': StockItem.Category.CHEESE, 'unit': 'kg', 'par_level': 8.0, 'price_per_unit': 1200.00},
            
            # Sauce
            {'stock_item_id': 'SAUCE001', 'name': 'Sauce Tomate', 'category': StockItem.Category.SAUCE, 'unit': 'L', 'par_level': 25.0, 'price_per_unit': 350.00},
            {'stock_item_id': 'SAUCE002', 'name': 'Sauce Barbecue', 'category': StockItem.Category.SAUCE, 'unit': 'L', 'par_level': 12.0, 'price_per_unit': 450.00},
            {'stock_item_id': 'SAUCE003', 'name': 'Huile d\'olive', 'category': StockItem.Category.SAUCE, 'unit': 'L', 'par_level': 10.0, 'price_per_unit': 600.00},
            
            # Meat
            {'stock_item_id': 'MEAT001', 'name': 'Poulet', 'category': StockItem.Category.MEAT, 'unit': 'kg', 'par_level': 15.0, 'price_per_unit': 1400.00},
            {'stock_item_id': 'MEAT002', 'name': 'Pepperoni', 'category': StockItem.Category.MEAT, 'unit': 'kg', 'par_level': 12.0, 'price_per_unit': 1500.00},
            {'stock_item_id': 'MEAT003', 'name': 'Viande Hachée', 'category': StockItem.Category.MEAT, 'unit': 'kg', 'par_level': 10.0, 'price_per_unit': 1300.00},
            {'stock_item_id': 'MEAT004', 'name': 'Merguez', 'category': StockItem.Category.MEAT, 'unit': 'kg', 'par_level': 8.0, 'price_per_unit': 1600.00},
            {'stock_item_id': 'MEAT005', 'name': 'Salamé Poulet', 'category': StockItem.Category.MEAT, 'unit': 'kg', 'par_level': 6.0, 'price_per_unit': 1450.00},
            {'stock_item_id': 'MEAT006', 'name': 'Thon', 'category': StockItem.Category.MEAT, 'unit': 'kg', 'par_level': 5.0, 'price_per_unit': 1800.00},
            {'stock_item_id': 'MEAT007', 'name': 'Anchois', 'category': StockItem.Category.MEAT, 'unit': 'kg', 'par_level': 3.0, 'price_per_unit': 2000.00},
            {'stock_item_id': 'MEAT008', 'name': 'Crevettes', 'category': StockItem.Category.MEAT, 'unit': 'kg', 'par_level': 4.0, 'price_per_unit': 2200.00},
            
            # Vegetables
            {'stock_item_id': 'VEG001', 'name': 'Tomates en dés', 'category': StockItem.Category.VEG, 'unit': 'kg', 'par_level': 8.0, 'price_per_unit': 400.00},
            {'stock_item_id': 'VEG002', 'name': 'Poivron', 'category': StockItem.Category.VEG, 'unit': 'kg', 'par_level': 7.0, 'price_per_unit': 500.00},
            {'stock_item_id': 'VEG003', 'name': 'Oignon rouge', 'category': StockItem.Category.VEG, 'unit': 'kg', 'par_level': 10.0, 'price_per_unit': 300.00},
            {'stock_item_id': 'VEG004', 'name': 'Olives noires', 'category': StockItem.Category.VEG, 'unit': 'kg', 'par_level': 6.0, 'price_per_unit': 800.00},
            {'stock_item_id': 'VEG005', 'name': 'Champignons', 'category': StockItem.Category.VEG, 'unit': 'kg', 'par_level': 5.0, 'price_per_unit': 600.00},
            {'stock_item_id': 'VEG006', 'name': 'Oignon', 'category': StockItem.Category.VEG, 'unit': 'kg', 'par_level': 9.0, 'price_per_unit': 250.00},
            {'stock_item_id': 'VEG007', 'name': 'Câpres', 'category': StockItem.Category.VEG, 'unit': 'kg', 'par_level': 2.0, 'price_per_unit': 900.00},
            {'stock_item_id': 'VEG008', 'name': 'Basilic', 'category': StockItem.Category.VEG, 'unit': 'kg', 'par_level': 1.0, 'price_per_unit': 700.00},
            {'stock_item_id': 'VEG009', 'name': 'Herbes italiennes', 'category': StockItem.Category.VEG, 'unit': 'kg', 'par_level': 2.0, 'price_per_unit': 850.00},
            
            # Beverages
            {'stock_item_id': 'BEV001', 'name': 'Hamoud Boualem 1L', 'category': StockItem.Category.BEVERAGE, 'unit': 'bottle', 'par_level': 50.0, 'price_per_unit': 80.00},
            {'stock_item_id': 'BEV002', 'name': 'Hamoud Boualem 24cL', 'category': StockItem.Category.BEVERAGE, 'unit': 'can', 'par_level': 100.0, 'price_per_unit': 40.00},
            {'stock_item_id': 'BEV003', 'name': 'Hamoud Boualem 33cL', 'category': StockItem.Category.BEVERAGE, 'unit': 'bottle', 'par_level': 80.0, 'price_per_unit': 50.00},
            {'stock_item_id': 'BEV004', 'name': 'IFRUIT 1L', 'category': StockItem.Category.BEVERAGE, 'unit': 'bottle', 'par_level': 40.0, 'price_per_unit': 120.00},
            {'stock_item_id': 'BEV005', 'name': 'IFRUIT 33CL', 'category': StockItem.Category.BEVERAGE, 'unit': 'bottle', 'par_level': 60.0, 'price_per_unit': 60.00},
            {'stock_item_id': 'BEV006', 'name': 'N\'Gaous 1L', 'category': StockItem.Category.BEVERAGE, 'unit': 'bottle', 'par_level': 30.0, 'price_per_unit': 100.00},
            {'stock_item_id': 'BEV007', 'name': 'N\'Gaous 20CL', 'category': StockItem.Category.BEVERAGE, 'unit': 'bottle', 'par_level': 50.0, 'price_per_unit': 30.00},
            {'stock_item_id': 'BEV008', 'name': 'Rouiba 1L', 'category': StockItem.Category.BEVERAGE, 'unit': 'bottle', 'par_level': 35.0, 'price_per_unit': 90.00},
            {'stock_item_id': 'BEV009', 'name': 'Rouiba 20CL', 'category': StockItem.Category.BEVERAGE, 'unit': 'bottle', 'par_level': 55.0, 'price_per_unit': 25.00},
            {'stock_item_id': 'BEV010', 'name': 'Eau Minérale 1.5L', 'category': StockItem.Category.BEVERAGE, 'unit': 'bottle', 'par_level': 60.0, 'price_per_unit': 40.00},
            {'stock_item_id': 'BEV011', 'name': 'Eau Minérale 50CL', 'category': StockItem.Category.BEVERAGE, 'unit': 'bottle', 'par_level': 80.0, 'price_per_unit': 20.00},
            {'stock_item_id': 'BEV012', 'name': 'Eau Minérale 33CL', 'category': StockItem.Category.BEVERAGE, 'unit': 'bottle', 'par_level': 100.0, 'price_per_unit': 15.00},
            {'stock_item_id': 'BEV013', 'name': 'Vichy 33cl', 'category': StockItem.Category.BEVERAGE, 'unit': 'bottle', 'par_level': 40.0, 'price_per_unit': 45.00},
            
            # Packaging
            {'stock_item_id': 'PACK001', 'name': 'Boîte Pizza Grande', 'category': StockItem.Category.PACKAGING, 'unit': 'piece', 'par_level': 300.0, 'price_per_unit': 30.00},
            {'stock_item_id': 'PACK002', 'name': 'Boîte Pizza Moyenne', 'category': StockItem.Category.PACKAGING, 'unit': 'piece', 'par_level': 200.0, 'price_per_unit': 25.00},
            {'stock_item_id': 'PACK003', 'name': 'Boîte Pizza Petite', 'category': StockItem.Category.PACKAGING, 'unit': 'piece', 'par_level': 150.0, 'price_per_unit': 20.00},
        ]

        for item_data in stock_data:
            stock_item = StockItem.objects.create(**item_data)
            self.stock_items.append(stock_item)

    def create_menus_and_items(self):
        """Create menus and menu items with exact items from your list"""
        print("Creating menus and items...")
        
        # Create a menu for each store
        for store in self.stores:
            menu = Menu.objects.create(store=store)
            self.menus.append(menu)
            
            # PIZZAS
            pizza_items = [
                {
                    'name': {'fr': 'Mix de viandes', 'en': 'Mixed Meats'},
                    'description': {'fr': 'Mozzarella, tomates en dés, poulet, peperoni, viande hachée', 'en': 'Mozzarella, diced tomatoes, chicken, pepperoni, ground meat'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 700,  
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'MEAT001', 'qty': 0.08},
                        {'stockItemId': 'MEAT002', 'qty': 0.06},
                        {'stockItemId': 'MEAT003', 'qty': 0.06},
                        {'stockItemId': 'VEG001', 'qty': 0.05}
                    ]
                },
                {
                    'name': {'fr': 'Merguez', 'en': 'Merguez'},
                    'description': {'fr': 'Mozzarella, poivron, merguez, olives noires', 'en': 'Mozzarella, bell peppers, merguez, black olives'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 400,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'MEAT004', 'qty': 0.1},
                        {'stockItemId': 'VEG002', 'qty': 0.06},
                        {'stockItemId': 'VEG004', 'qty': 0.03}
                    ]
                },
                {
                    'name': {'fr': 'Pepperoni', 'en': 'Pepperoni'},
                    'description': {'fr': 'Mozzarella, pepperoni', 'en': 'Mozzarella, pepperoni'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 600,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'MEAT002', 'qty': 0.12}
                    ]
                },
                {
                    'name': {'fr': 'Pepperoni & Tomates', 'en': 'Pepperoni & Tomatoes'},
                    'description': {'fr': 'Mozzarella, tomates en dés, pepperoni', 'en': 'Mozzarella, diced tomatoes, pepperoni'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 650,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'MEAT002', 'qty': 0.1},
                        {'stockItemId': 'VEG001', 'qty': 0.06}
                    ]
                },
                {
                    'name': {'fr': 'Viande hachée', 'en': 'Ground Meat'},
                    'description': {'fr': 'Mozzarella, viande hachée', 'en': 'Mozzarella, ground meat'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 500,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'MEAT003', 'qty': 0.12}
                    ]
                },
                {
                    'name': {'fr': 'Poulet barbecue', 'en': 'BBQ Chicken'},
                    'description': {'fr': 'Mozzarella, Poulet, oignon rouge, Salamé Poulet, Sauce barbecue', 'en': 'Mozzarella, Chicken, red onion, Chicken Salami, BBQ sauce'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 450,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE002', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'MEAT001', 'qty': 0.1},
                        {'stockItemId': 'VEG003', 'qty': 0.04},
                        {'stockItemId': 'MEAT005', 'qty': 0.05}
                    ]
                },
                {
                    'name': {'fr': 'Légumes & poulet', 'en': 'Vegetables & Chicken'},
                    'description': {'fr': 'Mozzarella, Poulet, tomates en dés, poivron, oignon', 'en': 'Mozzarella, Chicken, diced tomatoes, bell peppers, onion'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 500,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'MEAT001', 'qty': 0.1},
                        {'stockItemId': 'VEG001', 'qty': 0.05},
                        {'stockItemId': 'VEG002', 'qty': 0.05},
                        {'stockItemId': 'VEG006', 'qty': 0.04}
                    ]
                },
                {
                    'name': {'fr': 'Double chicken', 'en': 'Double Chicken'},
                    'description': {'fr': 'Mozzarella, Double Poulet', 'en': 'Mozzarella, Double Chicken'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 600,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'MEAT001', 'qty': 0.2}
                    ]
                },
                {
                    'name': {'fr': 'Margherita', 'en': 'Margherita'},
                    'description': {'fr': 'Mozzarella, tomates en dés, Herbes italiennes, Huile d\'olive', 'en': 'Mozzarella, diced tomatoes, Italian herbs, Olive oil'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 350,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'VEG001', 'qty': 0.06},
                        {'stockItemId': 'VEG009', 'qty': 0.02},
                        {'stockItemId': 'SAUCE003', 'qty': 0.02}
                    ]
                },
                {
                    'name': {'fr': 'Végétarienne', 'en': 'Vegetarian'},
                    'description': {'fr': 'Mozzarella, tomates en dés, poivron, oignon rouge, Herbes italiennes', 'en': 'Mozzarella, diced tomatoes, bell peppers, red onion, Italian herbs'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 450,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'VEG001', 'qty': 0.05},
                        {'stockItemId': 'VEG002', 'qty': 0.05},
                        {'stockItemId': 'VEG003', 'qty': 0.04},
                        {'stockItemId': 'VEG009', 'qty': 0.02}
                    ]
                },
                {
                    'name': {'fr': 'Végétarienne champignons', 'en': 'Mushroom Vegetarian'},
                    'description': {'fr': 'Mozzarella, Champignons, tomates en dés, poivron, oignon rouge, Herbes italiennes', 'en': 'Mozzarella, Mushrooms, diced tomatoes, bell peppers, red onion, Italian herbs'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 650,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'VEG005', 'qty': 0.08},
                        {'stockItemId': 'VEG001', 'qty': 0.05},
                        {'stockItemId': 'VEG002', 'qty': 0.05},
                        {'stockItemId': 'VEG003', 'qty': 0.04},
                        {'stockItemId': 'VEG009', 'qty': 0.02}
                    ]
                },
                {
                    'name': {'fr': '3 fromages', 'en': '3 Cheeses'},
                    'description': {'fr': 'Mozzarella, cheddar, gruyère', 'en': 'Mozzarella, cheddar, gruyère'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 500,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.1},
                        {'stockItemId': 'CHEESE002', 'qty': 0.05},
                        {'stockItemId': 'CHEESE003', 'qty': 0.05}
                    ]
                },
                {
                    'name': {'fr': 'Tuna', 'en': 'Tuna'},
                    'description': {'fr': 'Mozzarella, thon, olives noires, basilic', 'en': 'Mozzarella, tuna, black olives, basil'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 450,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'MEAT006', 'qty': 0.1},
                        {'stockItemId': 'VEG004', 'qty': 0.03},
                        {'stockItemId': 'VEG008', 'qty': 0.01}
                    ]
                },
                {
                    'name': {'fr': 'Anchovis', 'en': 'Anchovies'},
                    'description': {'fr': 'Mozzarella, anchois, câpres, Huile d\'olive', 'en': 'Mozzarella, anchovies, capers, Olive oil'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 700,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'MEAT007', 'qty': 0.08},
                        {'stockItemId': 'VEG007', 'qty': 0.02},
                        {'stockItemId': 'SAUCE003', 'qty': 0.02}
                    ]
                },
                {
                    'name': {'fr': 'Crevette', 'en': 'Shrimp'},
                    'description': {'fr': 'Mozzarella, crevettes, poivron', 'en': 'Mozzarella, shrimp, bell peppers'},
                    'category': MenuItem.Category.PIZZA,
                    'prices': 800,
                    'recipe': [
                        {'stockItemId': 'DOUGH001', 'qty': 0.25},
                        {'stockItemId': 'SAUCE001', 'qty': 0.08},
                        {'stockItemId': 'CHEESE001', 'qty': 0.15},
                        {'stockItemId': 'MEAT008', 'qty': 0.12},
                        {'stockItemId': 'VEG002', 'qty': 0.06}
                    ]
                },
            ]

            # Create pizza items with sizes
            for pizza in pizza_items:
                for i, size in enumerate(['S']):
                    menu_item = MenuItem.objects.create(
                        menu=menu,
                        name=pizza['name'],
                        description=pizza['description'],
                        category=pizza['category'],
                        price=Decimal(str(pizza['prices'])),
                        recipe=pizza['recipe'],
                        display_type=MenuItem.DisplayType.NORMAL,
                        available=True
                    )
                    self.menu_items.append(menu_item)

            # DESSERTS
            desserts = [
                {'name': {'fr': 'Mousse au Chocolat', 'en': 'Chocolate Mousse'}, 'price': 300},
                {'name': {'fr': 'Fondant au chocolat', 'en': 'Chocolate Fondant'}, 'price': 350},
                {'name': {'fr': 'Cheese cup Oreo', 'en': 'Oreo Cheese Cup'}, 'price': 250},
                {'name': {'fr': 'Tiramisu caramel', 'en': 'Caramel Tiramisu'}, 'price': 320},
                {'name': {'fr': 'Tiramisu cacao', 'en': 'Cocoa Tiramisu'}, 'price': 320},
                {'name': {'fr': 'Cheese cup Lotus', 'en': 'Lotus Cheese Cup'}, 'price': 250},
                {'name': {'fr': 'Cheese cup Fraise', 'en': 'Strawberry Cheese Cup'}, 'price': 250},
                {'name': {'fr': 'Cheese cake Original', 'en': 'Original Cheesecake'}, 'price': 400},
                {'name': {'fr': 'Cheese cup Pistache', 'en': 'Pistachio Cheese Cup'}, 'price': 280},
            ]

            for dessert in desserts:
                menu_item = MenuItem.objects.create(
                    menu=menu,
                    name=dessert['name'],
                    description={'fr': 'Délicieux dessert', 'en': 'Delicious dessert'},
                    category=MenuItem.Category.DESSERT,
                    price=Decimal(str(dessert['price'])),
                    recipe=[],
                    display_type=MenuItem.DisplayType.NORMAL,
                    available=True
                )
                self.menu_items.append(menu_item)

            # COLD DRINKS
            cold_drinks = [
                {'name': {'fr': 'Hamoud Boualem 1L', 'en': 'Hamoud Boualem 1L'}, 'price': 100, 'stock_id': 'BEV001'},
                {'name': {'fr': 'Hamoud Boualem 24cL Canette', 'en': 'Hamoud Boualem 24cL Can'}, 'price': 50, 'stock_id': 'BEV002'},
                {'name': {'fr': 'Hamoud Boualem 33cL', 'en': 'Hamoud Boualem 33cL'}, 'price': 60, 'stock_id': 'BEV003'},
                {'name': {'fr': 'IFRUIT 1L', 'en': 'IFRUIT 1L'}, 'price': 150, 'stock_id': 'BEV004'},
                {'name': {'fr': 'IFRUIT 33CL', 'en': 'IFRUIT 33CL'}, 'price': 70, 'stock_id': 'BEV005'},
                {'name': {'fr': 'N\'Gaous 1L', 'en': 'N\'Gaous 1L'}, 'price': 120, 'stock_id': 'BEV006'},
                {'name': {'fr': 'N\'Gaous 20CL', 'en': 'N\'Gaous 20CL'}, 'price': 40, 'stock_id': 'BEV007'},
                {'name': {'fr': 'Rouiba 1L', 'en': 'Rouiba 1L'}, 'price': 110, 'stock_id': 'BEV008'},
                {'name': {'fr': 'Rouiba 20CL', 'en': 'Rouiba 20CL'}, 'price': 35, 'stock_id': 'BEV009'},
                {'name': {'fr': 'Eau Minérale 1.5L', 'en': 'Mineral Water 1.5L'}, 'price': 50, 'stock_id': 'BEV010'},
                {'name': {'fr': 'Eau Minérale 50CL', 'en': 'Mineral Water 50CL'}, 'price': 25, 'stock_id': 'BEV011'},
                {'name': {'fr': 'Eau Minérale 33CL', 'en': 'Mineral Water 33CL'}, 'price': 20, 'stock_id': 'BEV012'},
                {'name': {'fr': 'Vichy 33cl', 'en': 'Vichy 33cl'}, 'price': 55, 'stock_id': 'BEV013'},
            ]

            for drink in cold_drinks:
                menu_item = MenuItem.objects.create(
                    menu=menu,
                    name=drink['name'],
                    description={'fr': 'Boisson fraîche', 'en': 'Cold drink'},
                    category=MenuItem.Category.COLD_DRINK,
                    price=Decimal(str(drink['price'])),
                    recipe=[{'stockItemId': drink['stock_id'], 'qty': 1}],
                    display_type=MenuItem.DisplayType.NORMAL,
                    available=True
                )
                self.menu_items.append(menu_item)

            # GELATO (placeholder - check availability)
            gelato = MenuItem.objects.create(
                menu=menu,
                name={'fr': 'Gelato', 'en': 'Gelato'},
                description={'fr': 'Vérifiez la disponibilité', 'en': 'Check availability'},
                category=MenuItem.Category.GELATO,
                price=Decimal('200'),
                recipe=[],
                display_type=MenuItem.DisplayType.NORMAL,
                available=False
            )
            self.menu_items.append(gelato)

            # HOT DRINKS (placeholder)
            hot_drinks = [
                {'name': {'fr': 'Café', 'en': 'Coffee'}, 'price': 40},
                {'name': {'fr': 'Thé', 'en': 'Tea'}, 'price': 30},
            ]

            for drink in hot_drinks:
                menu_item = MenuItem.objects.create(
                    menu=menu,
                    name=drink['name'],
                    description={'fr': 'Boisson chaude', 'en': 'Hot drink'},
                    category=MenuItem.Category.HOT_DRINK,
                    price=Decimal(str(drink['price'])),
                    recipe=[],
                    display_type=MenuItem.DisplayType.NORMAL,
                    available=True
                )
                self.menu_items.append(menu_item)

    def create_orders(self):
        """Create sample orders with Algerian context"""
        print("Creating orders...")
        
        order_data = [
            {
                'store': self.stores[0],
                'user': self.users[1],
                'display_id': f'NX{random.randint(1000, 9999)}',
                'created_at': timezone.now() - timedelta(days=2, hours=5),
                'pickup_type': Order.PickupType.DELIVERY,
                'status': Order.Status.COMPLETED,
                'items': [
                    {
                        'itemId': self.menu_items[0].item_id,  # Mix de viandes S
                        'name': {'fr': 'Mix de viandes', 'en': 'Mixed Meats'},
                        'qty': 1,
                        'size': 'S',
                        'price': 700.00,
                        'addedIngredients': ['CHEESE001'],  # Extra cheese
                        'removedIngredients': []
                    },
                    {
                        'itemId': self.menu_items[45].item_id,  # Hamoud Boualem 1L
                        'name': {'fr': 'Hamoud Boualem 1L', 'en': 'Hamoud Boualem 1L'},
                        'qty': 1,
                        'size': '1L',
                        'price': 100.00,
                        'addedIngredients': [],
                        'removedIngredients': []
                    }
                ],
                'total': 800.00,
                'payment': {'method': 'ONLINE', 'paid': True, 'amount': 800.00},
                'source': Order.Source.MOBILE_APP,
                'meta': {'delivery_address': '456 Rue Hassiba Ben Bouali, Alger', 'special_instructions': 'Sonner à la porte'}
            },
            {
                'store': self.stores[1],
                'user': self.users[2],
                'display_id': f'NX{random.randint(1000, 9999)}',
                'created_at': timezone.now() - timedelta(days=1, hours=3),
                'pickup_type': Order.PickupType.TAKEAWAY,
                'status': Order.Status.READY,
                'items': [
                    {
                        'itemId': self.menu_items[3].item_id,  # Merguez M
                        'name': {'fr': 'Merguez', 'en': 'Merguez'},
                        'qty': 2,
                        'size': 'M',
                        'price': 550.00,
                        'addedIngredients': ['VEG002'],  # Extra peppers
                        'removedIngredients': ['VEG004']  # Remove olives
                    }
                ],
                'total': 1100.00,
                'payment': {'method': 'CARD', 'paid': True, 'amount': 1100.00},
                'source': Order.Source.WEBSITE,
                'meta': {'special_instructions': 'Bien cuite'}
            }
        ]

        for order_info in order_data:
            order = Order.objects.create(**order_info)
            self.orders.append(order)

    def seed(self):
        """Run the complete seeding process"""
        print("Starting database seeding...")
        
        self.clear_database()
        self.create_users()
        self.create_stores()
        self.create_stock_items()
        self.create_menus_and_items()
        self.create_orders()
        
        print("Database seeding completed successfully!")
        print(f"Created: {len(self.users)} users, {len(self.stores)} stores, {len(self.stock_items)} stock items")
        print(f"Created: {len(self.menus)} menus, {len(self.menu_items)} menu items, {len(self.orders)} orders")
        
        # Display sample data
        print("\nSample Menu Items:")
        for i, item in enumerate(self.menu_items[:5]):
            print(f"- {item.name['fr']}: {item.price} DA")

if __name__ == '__main__':
    seeder = DatabaseSeeder()
    seeder.seed()