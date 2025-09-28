import 'package:get/get.dart';
import 'package:flutter/material.dart';
import 'package:nexo_pizza_staff/Data_Mangement/models/product_model.dart';
import 'package:nexo_pizza_staff/Data_Mangement/models/order_models.dart';
import 'package:nexo_pizza_staff/Data_Mangement/services/order_service.dart';

class OrderCntrl extends GetxController {
  final OrderService _orderService = OrderService();
  
  var supplierValue = 'Select Supplier'.obs;
  var productValue = 'Add Product'.obs;
  var products = <ProductModel>[].obs;
  var selectedProducts = <ProductModel>[].obs;
  var availableProducts = <Product>[].obs;
  var orders = <Order>[].obs;
  var isLoading = false.obs;
  var isCreatingOrder = false.obs;

  final TextEditingController notesController = TextEditingController();

  @override
  void onInit() {
    super.onInit();
    loadProducts();
    loadOrders();
  }

  @override
  void onClose() {
    notesController.dispose();
    super.onClose();
  }

  // Load available products from API
  Future<void> loadProducts() async {
    try {
      isLoading.value = true;
      final response = await _orderService.getProducts(limit: 100);
      availableProducts.value = response.products;
    } catch (e) {
      Get.snackbar(
        'Error',
        'Failed to load products: $e',
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: Colors.red,
        colorText: Colors.white,
      );
    } finally {
      isLoading.value = false;
    }
  }

  // Load orders from API
  Future<void> loadOrders() async {
    try {
      isLoading.value = true;
      final response = await _orderService.getOrders();
      orders.value = response.orders;
    } catch (e) {
      Get.snackbar(
        'Error',
        'Failed to load orders: $e',
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: Colors.red,
        colorText: Colors.white,
      );
    } finally {
      isLoading.value = false;
    }
  }

  // Add product to order
  void addProductToOrder(Product product, double quantity) {
    final existingIndex = selectedProducts.indexWhere((p) => p.id == product.id);
    
    if (existingIndex != -1) {
      // Update existing product quantity
      selectedProducts[existingIndex].quantity = 
          (selectedProducts[existingIndex].quantity ?? 0) + quantity;
    } else {
      // Add new product
      selectedProducts.add(ProductModel(
        id: product.id,
        name: product.name,
        quantity: quantity,
        price: product.price,
        categoryId: product.categoryId,
        description: product.description,
      ));
    }
    
    // Also add to the existing products list for backward compatibility
    products.value = selectedProducts;
    update();
  }

  // Remove product from order
  void removeProductFromOrder(String productId) {
    selectedProducts.removeWhere((p) => p.id == productId);
    products.value = selectedProducts;
    update();
  }

  // Create order
  Future<bool> createOrder() async {
    if (selectedProducts.isEmpty) {
      Get.snackbar(
        'Error',
        'Please add at least one product to the order',
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: Colors.red,
        colorText: Colors.white,
      );
      return false;
    }

    try {
      isCreatingOrder.value = true;

      final orderItems = selectedProducts.map((product) => OrderItem(
        productId: product.id!,
        quantity: product.quantity!.toInt(),
        unitPrice: product.price ?? 0.0,
      )).toList();

      final orderRequest = CreateOrderRequest(
        items: orderItems,
        notes: notesController.text.isNotEmpty ? notesController.text : null,
      );

      final orderId = await _orderService.createOrder(orderRequest);

      if (orderId != null) {
        Get.snackbar(
          'Success',
          'Order created successfully!',
          snackPosition: SnackPosition.BOTTOM,
          backgroundColor: Colors.green,
          colorText: Colors.white,
        );

        // Clear the order
        clearOrder();
        
        // Reload orders to get the latest data
        await loadOrders();
        
        return true;
      }
      return false;
    } catch (e) {
      Get.snackbar(
        'Error',
        'Failed to create order: $e',
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: Colors.red,
        colorText: Colors.white,
      );
      return false;
    } finally {
      isCreatingOrder.value = false;
    }
  }

  // Clear current order
  void clearOrder() {
    selectedProducts.clear();
    products.clear();
    notesController.clear();
    supplierValue.value = 'Select Supplier';
    productValue.value = 'Add Product';
    update();
  }

  // Get total amount for current order
  double get totalAmount {
    return selectedProducts.fold(0.0, (sum, product) => 
        sum + ((product.price ?? 0.0) * (product.quantity ?? 0.0)));
  }

  // Get total items count
  int get totalItems {
    return selectedProducts.fold(0, (sum, product) => 
        sum + (product.quantity?.toInt() ?? 0));
  }
}
