import 'package:dio/dio.dart';
import '../models/order_models.dart';
import 'api_service.dart';

class OrderService {
  final ApiService _apiService = ApiService();

  // Create a new order
  Future<String?> createOrder(CreateOrderRequest orderRequest) async {
    try {
      final response = await _apiService.dio.post(
        '/orders',
        data: orderRequest.toJson(),
      );

      if (response.statusCode == 201) {
        return response.data['orderId'];
      }
      return null;
    } on DioException catch (e) {
      print('Error creating order: ${e.message}');
      throw Exception('Failed to create order: ${e.response?.data['message'] ?? e.message}');
    }
  }

  // Get orders with filters
  Future<OrdersResponse> getOrders({
    String? orderNumber,
    String? staffId,
    String? status,
    String? sortBy,
    String? order,
    int page = 1,
    int limit = 10,
  }) async {
    try {
      final queryParams = <String, dynamic>{
        'page': page,
        'limit': limit,
      };

      if (orderNumber != null) queryParams['orderNumber'] = orderNumber;
      if (staffId != null) queryParams['staffId'] = staffId;
      if (status != null) queryParams['status'] = status;
      if (sortBy != null) queryParams['sortBy'] = sortBy;
      if (order != null) queryParams['order'] = order;

      final response = await _apiService.dio.get(
        '/orders',
        queryParameters: queryParams,
      );

      if (response.statusCode == 200) {
        return OrdersResponse.fromJson(response.data);
      }
      return OrdersResponse(orders: [], total: 0, pages: 0);
    } on DioException catch (e) {
      print('Error fetching orders: ${e.message}');
      throw Exception('Failed to fetch orders: ${e.response?.data['message'] ?? e.message}');
    }
  }

  // Get a specific order by ID
  Future<Order?> getOrderById(String orderId) async {
    try {
      final response = await _apiService.dio.get('/orders/$orderId');

      if (response.statusCode == 200) {
        return Order.fromJson(response.data['order']);
      }
      return null;
    } on DioException catch (e) {
      print('Error fetching order: ${e.message}');
      throw Exception('Failed to fetch order: ${e.response?.data['message'] ?? e.message}');
    }
  }

  // Get products for order creation
  Future<ProductsResponse> getProducts({
    String? name,
    String? categoryId,
    String? sortBy,
    String? order,
    int page = 1,
    int limit = 10,
  }) async {
    try {
      final queryParams = <String, dynamic>{
        'page': page,
        'limit': limit,
      };

      if (name != null) queryParams['name'] = name;
      if (categoryId != null) queryParams['categoryId'] = categoryId;
      if (sortBy != null) queryParams['sortBy'] = sortBy;
      if (order != null) queryParams['order'] = order;

      final response = await _apiService.dio.get(
        '/products',
        queryParameters: queryParams,
      );

      if (response.statusCode == 200) {
        return ProductsResponse.fromJson(response.data);
      }
      return ProductsResponse(products: [], total: 0, pages: 0);
    } on DioException catch (e) {
      print('Error fetching products: ${e.message}');
      throw Exception('Failed to fetch products: ${e.response?.data['message'] ?? e.message}');
    }
  }
}