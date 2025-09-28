# Nexo Pizza Staff - Order Management Integration

This document explains the integration between the Flutter staff app and the Node.js backend API for order management.

## Features Implemented

### 🍕 Order Management
- **Create Orders**: Staff can create new orders by selecting products and quantities
- **View Orders**: Display all orders with real-time data from the API
- **Product Selection**: Browse available products with prices from the backend
- **Order Summary**: Real-time calculation of totals and item counts

### 🔌 API Integration
- **RESTful API**: Complete integration with the nexo-back Node.js server
- **Authentication**: Token-based authentication with cookie management
- **Real-time Updates**: Automatic refresh of orders and products
- **Error Handling**: Proper error messages and loading states

### 📱 UI/UX Improvements
- **Loading States**: Beautiful loading animations during API calls
- **Empty States**: Informative messages when no data is available  
- **Pull to Refresh**: Swipe down to refresh orders list
- **Product Management**: Add/remove products with quantity and price display
- **Order Summary**: Live calculation of totals and item counts

## Backend API Endpoints Used

### Orders
- `POST /api/orders` - Create a new order
- `GET /api/orders` - Get all orders with filters
- `GET /api/orders/:id` - Get specific order details

### Products  
- `GET /api/products` - Get all products for order creation

## Files Modified/Created

### New Files
- `lib/Data_Mangement/services/api_service.dart` - HTTP service configuration
- `lib/Data_Mangement/services/order_service.dart` - Order API calls
- `lib/Data_Mangement/models/order_models.dart` - Order data models

### Modified Files
- `lib/State_Management/order_cntrl.dart` - Enhanced with API integration
- `lib/Data_Mangement/models/product_model.dart` - Added price and ID fields
- `lib/HomePagaesStaff/add_order.dart` - Connected with API, improved UI
- `lib/HomePagaesStaff/orders_staff.dart` - Display real orders from API
- `lib/Data_Mangement/bindings/auth_binding.dart` - Added OrderCntrl initialization

## How to Run

### 1. Start the Backend Server
```bash
cd nexo-back
npm install
npm run dev
```
The server will run on `http://localhost:5000`

### 2. Update API Configuration
Make sure the API base URL in `lib/Data_Mangement/services/api_service.dart` matches your backend:
```dart
static const String baseUrl = 'http://YOUR_IP:5000/api';
```

### 3. Run the Flutter App
```bash
cd nexo_pizza_staff
flutter pub get
flutter run
```

## Usage Instructions

### Creating an Order
1. Navigate to the "Add Order" page (middle tab)
2. Select products by tapping the "+" button
3. Choose products from the list with prices
4. Enter quantities for each product
5. Add notes if needed
6. Review the order summary
7. Tap "Create Order" to submit

### Viewing Orders
1. Navigate to "My Orders" page (right tab)
2. Pull down to refresh the list
3. View order details including:
   - Order number
   - Creation date
   - Total items and amount
   - Order status

## API Response Examples

### Create Order Request
```json
{
  "items": [
    {
      "productId": "product_id_here",
      "quantity": 10,
      "unitPrice": 25.50
    }
  ],
  "notes": "Order notes here"
}
```

### Orders List Response
```json
{
  "orders": [
    {
      "_id": "order_id",
      "orderNumber": "ORD-20250928-1234",
      "items": [...],
      "totalAmount": 255.00,
      "status": "pending",
      "createdAt": "2025-09-28T10:00:00Z"
    }
  ],
  "total": 1,
  "pages": 1
}
```

## Error Handling

The app includes comprehensive error handling:
- Network connectivity issues
- Server errors
- Invalid data responses
- Authentication failures

All errors are displayed to users with helpful messages and suggested actions.

## Next Steps

1. **Authentication Integration**: Connect with the auth system for user-specific orders
2. **Order Status Updates**: Add functionality to update order status
3. **Image Upload**: Implement image upload for order receipts
4. **Push Notifications**: Add real-time order updates
5. **Offline Support**: Cache orders for offline viewing

---

*This integration provides a complete order management system connecting the Flutter staff app with the Node.js backend API.*