class OrderItem {
  final String productId;
  final int quantity;
  final double unitPrice;
  final DateTime? expirationDate;
  final String? productName;

  OrderItem({
    required this.productId,
    required this.quantity,
    required this.unitPrice,
    this.expirationDate,
    this.productName,
  });

  Map<String, dynamic> toJson() {
    return {
      'productId': productId,
      'quantity': quantity,
      'unitPrice': unitPrice,
      'expirationDate': expirationDate?.toIso8601String(),
    };
  }

  factory OrderItem.fromJson(Map<String, dynamic> json) {
    return OrderItem(
      productId: json['productId'] ?? '',
      quantity: json['quantity'] ?? 0,
      unitPrice: (json['unitPrice'] ?? 0).toDouble(),
      expirationDate: json['expirationDate'] != null 
          ? DateTime.parse(json['expirationDate']) 
          : null,
      productName: json['productName'],
    );
  }
}

class CreateOrderRequest {
  final List<OrderItem> items;
  final String? supplierId;
  final String? notes;

  CreateOrderRequest({
    required this.items,
    this.supplierId,
    this.notes,
  });

  Map<String, dynamic> toJson() {
    return {
      'items': items.map((item) => item.toJson()).toList(),
      'supplierId': supplierId,
      'notes': notes,
    };
  }
}

class Order {
  final String id;
  final String orderNumber;
  final List<OrderItem> items;
  final String? supplierId;
  final String staffId;
  final double totalAmount;
  final String? notes;
  final String status;
  final DateTime createdAt;
  final DateTime updatedAt;
  final String? bon;

  Order({
    required this.id,
    required this.orderNumber,
    required this.items,
    this.supplierId,
    required this.staffId,
    required this.totalAmount,
    this.notes,
    required this.status,
    required this.createdAt,
    required this.updatedAt,
    this.bon,
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
      id: json['_id'] ?? '',
      orderNumber: json['orderNumber'] ?? '',
      items: (json['items'] as List<dynamic>?)
          ?.map((item) => OrderItem.fromJson(item))
          .toList() ?? [],
      supplierId: json['supplierId'],
      staffId: json['staffId'] ?? '',
      totalAmount: (json['totalAmount'] ?? 0).toDouble(),
      notes: json['notes'],
      status: json['status'] ?? 'pending',
      createdAt: DateTime.parse(json['createdAt']),
      updatedAt: DateTime.parse(json['updatedAt']),
      bon: json['bon'],
    );
  }
}

class OrdersResponse {
  final List<Order> orders;
  final int total;
  final int pages;

  OrdersResponse({
    required this.orders,
    required this.total,
    required this.pages,
  });

  factory OrdersResponse.fromJson(Map<String, dynamic> json) {
    return OrdersResponse(
      orders: (json['orders'] as List<dynamic>?)
          ?.map((order) => Order.fromJson(order))
          .toList() ?? [],
      total: json['total'] ?? 0,
      pages: json['pages'] ?? 0,
    );
  }
}

class Product {
  final String id;
  final String name;
  final double price;
  final int quantity;
  final String? categoryId;
  final String? description;
  final DateTime createdAt;
  final DateTime updatedAt;

  Product({
    required this.id,
    required this.name,
    required this.price,
    required this.quantity,
    this.categoryId,
    this.description,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['_id'] ?? '',
      name: json['name'] ?? '',
      price: (json['price'] ?? 0).toDouble(),
      quantity: json['quantity'] ?? 0,
      categoryId: json['categoryId'],
      description: json['description'],
      createdAt: DateTime.parse(json['createdAt']),
      updatedAt: DateTime.parse(json['updatedAt']),
    );
  }
}

class ProductsResponse {
  final List<Product> products;
  final int total;
  final int pages;

  ProductsResponse({
    required this.products,
    required this.total,
    required this.pages,
  });

  factory ProductsResponse.fromJson(Map<String, dynamic> json) {
    return ProductsResponse(
      products: (json['products'] as List<dynamic>?)
          ?.map((product) => Product.fromJson(product))
          .toList() ?? [],
      total: json['total'] ?? 0,
      pages: json['pages'] ?? 0,
    );
  }
}