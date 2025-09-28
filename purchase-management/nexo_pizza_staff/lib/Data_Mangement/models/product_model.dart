class ProductModel {
  String? id;
  String? name;
  double? quantity;
  double? price;
  String? categoryId;
  String? description;

  ProductModel({
    this.id,
    this.name, 
    this.quantity,
    this.price,
    this.categoryId,
    this.description,
  });

  factory ProductModel.fromJson(Map<String, dynamic> json) {
    return ProductModel(
      id: json['_id'],
      name: json['name'],
      quantity: (json['quantity'] ?? 0).toDouble(),
      price: (json['price'] ?? 0).toDouble(),
      categoryId: json['categoryId'],
      description: json['description'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      '_id': id,
      'name': name,
      'quantity': quantity,
      'price': price,
      'categoryId': categoryId,
      'description': description,
    };
  }
}
