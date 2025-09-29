from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# ----------------------------
# USERS
# ----------------------------

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        USER = 'USER', 'User'

    uid = models.AutoField(primary_key=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pfp = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    nexo_coins = models.IntegerField(null=True, blank=True, default=0) # previously loyalty points
    xp = models.IntegerField(null=True, blank=True, default=0) # experience points for gamification
    level = models.IntegerField(null=True, blank=True, default=1) # user level based on xp
    prefs = models.JSONField(default=dict)  # e.g., {"cuisine": ["Italian", "Mexican"], "diet": "Vegetarian", "favorites": [itemId1, itemId2]}
    def __str__(self):
        return self.first_name + " " + self.last_name
    


# ----------------------------
# STORES
# ----------------------------


class Store(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255) 
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100)
    open_at = models.TimeField()
    close_at = models.TimeField()
    capacity = models.PositiveIntegerField(null=True, blank=True)
    features = models.JSONField(default=list)  # ["delivery", "takeaway", "kds"]

    def __str__(self):
        return self.name


# ----------------------------
# STOCK ITEMS
# ----------------------------
class StockItem(models.Model):
    class Category(models.TextChoices):
        DOUGH = "Dough"
        CHEESE = "Cheese"
        SAUCE = "Sauce"
        BEVERAGE = "Beverage"
        PACKAGING = "Packaging"
        MEAT = "Meat"
        VEG = "Vegetable"

    stock_item_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=Category.choices)
    unit = models.CharField(max_length=20)
    par_level = models.FloatField()
    price_per_unit = models.FloatField()

    def __str__(self):
        return self.name


# ----------------------------
# MENUS & ITEMS
# ----------------------------
class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="menus")


class MenuItem(models.Model):
    class DisplayType(models.TextChoices):
        NORMAL = "NORMAL"
        OPTIONAL = "OPTIONAL"
        COMBO = "COMBO"
        PROMO = "PROMO"

    class Category(models.TextChoices):
        PIZZA = "Pizza"
        SALAD = "Salad"
        DESSERT = "Dessert"
        COLD_DRINK = "Cold Drink"
        HOT_DRINK = "Hot Drink"
        GELATO = "Gelato"



    item_id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    name = models.JSONField(default=dict)  # {"en": "Margherita Pizza", "fr": "Pizza Marguerite"}
    category = models.CharField(max_length=100, choices=Category.choices)
    description = models.JSONField(blank=True, null=True, default=dict)  # {"en": "Delicious pizza", "fr": "Pizza délicieuse"}
    price = models.DecimalField(max_digits=8, decimal_places=2)
    recipe = models.JSONField(default=list)  # [{stockItemId, qty}]
    display_type = models.CharField(max_length=20, choices=DisplayType.choices)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# ----------------------------
# ORDERS
# ----------------------------
class Order(models.Model):
    class PickupType(models.TextChoices):
        TAKEAWAY = "Takeaway"
        DELIVERY = "Delivery"
        DINEIN = "DineIn"

    class Status(models.TextChoices):
        PENDING = "PENDING"
        CONFIRMED = "CONFIRMED"
        PREPARING = "PREPARING"
        READY = "READY"
        COMPLETED = "COMPLETED"
        CANCELLED = "CANCELLED"
    
    class PaymentMethod(models.TextChoices):
        CASH = "CASH"
        CARD = "CARD"
        ONLINE = "ONLINE"

    class Source(models.TextChoices):
        WEBSITE = "WEBSITE"
        MOBILE_APP = "MOBILE_APP"
        PHONE = "PHONE"
        IN_PERSON = "IN_PERSON"

    id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="orders")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    display_id = models.CharField(max_length=100, blank=True, null=True, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    pickup_type = models.CharField(max_length=20, choices=PickupType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    items = models.JSONField(default=list, null=False, blank=False)  # [{itemId, name, qty, size, price, addedIngredients, removedIngredients}]
    total = models.FloatField()
    payment = models.JSONField(default=dict)  # {method, paid, amount}
    source = models.CharField(max_length=50, choices=Source.choices, null=True, blank=True)
    meta = models.JSONField(null=True, blank=True) # for extra info like coupon code, delivery address, special instructions, etc.
    def __str__(self):
        return f"Order {self.display_id}"