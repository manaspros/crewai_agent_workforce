E-commerce Website for Handmade Crafts - Test Plan

1. Introduction
This document outlines the test plan for the E-commerce Website for Handmade Crafts, focusing specifically on testing the backend functionalities developed by Engineer 3, including Shopping Cart, Order Processing, Payment Integration, Product Reviews, Seller Order Management, Admin Order Management, and associated email notifications. The plan covers Unit, Integration, and End-to-End testing phases.

2. Test Scope
In Scope:
 - Shopping Cart Backend API Endpoints (GET, POST, PUT, DELETE /api/cart)
 - Order Creation Backend API Endpoint (POST /api/checkout/create-order)
 - Payment Initiation Backend API Endpoint (POST /api/checkout/initiate-payment)
 - Payment Webhook Backend Endpoint (POST /api/checkout/payment-webhook) - Simulation based on provided code
 - Customer Order History Backend API Endpoints (GET /api/customer/orders, GET /api/customer/orders/{order_id})
 - Product Reviews Backend API Endpoints (GET /api/products/{product_id}/reviews, POST /api/products/{product_id}/reviews)
 - Seller Order Management Backend API Endpoints (GET /api/seller/orders, GET /api/seller/orders/{order_id}, PUT /api/seller/orders/{order_id}/status)
 - Admin Order Management Backend API Endpoints (GET /api/admin/orders, GET /api/admin/orders/{order_id}, PUT /api/admin/orders/{order_id}/status)
 - Email Notification Triggers (Order Confirmation, Shipping Notification)

Out of Scope for Engineer 3's testing focus in this plan:
 - Frontend UI rendering details (covered in separate frontend test plans)
 - User Authentication/Authorization implementation details (covered in Engineer 1's plan)
 - Product/Category/Tag Management implementation details (covered in Engineer 2's plan)
 - Image Upload/Storage details (covered in Engineer 2's plan)
 - Advanced search, filtering, sorting beyond basic implementation
 - Seller Payout processing details
 - Messaging system

3. Test Objectives
 - Verify that all API endpoints function correctly according to specifications.
 - Ensure data consistency in the simulated database (in-memory dictionaries).
 - Validate business logic related to cart management, order creation, and status updates.
 - Confirm proper integration with simulated payment gateway webhook and email service.
 - Verify user roles and permissions are enforced for relevant endpoints.
 - Confirm end-to-end user flows involving Engineer 3's backend features are successful.

4. Test Types
 - Unit Testing: Testing individual backend functions or methods (conceptual, based on provided code structure).
 - Integration Testing: Testing the interaction between backend components (e.g., API endpoint -> database interaction, endpoint -> helper function, endpoint -> other endpoint in a flow).
 - End-to-End Testing: Testing full user journeys involving multiple backend endpoints and simulated frontend actions.

5. Test Environment
 - Backend: Local development environment running the provided Flask application code (or deployed test environment).
 - Simulated Database (in-memory dictionaries).
 - Simulated External Services (Payment Gateway Webhook, Email Service - via print statements/mocks).
 - Testing Tools: Postman/curl for API testing, or automated testing framework (e.g., Pytest with Flask test client, Selenium/Cypress for E2E - described conceptually).

6. Test Data
 - Pre-populated users (customer, seller, admin) with JWT tokens.
 - Pre-populated products with sufficient stock.
 - Sample shipping addresses.
 - Sample review data.
 - Initial state of carts and orders.

7. Entry Criteria
 - Backend code for Engineer 3's assignments is deployed to the test environment.
 - Simulated dependencies (DB, auth helpers) are functional.
 - Test data is set up.

8. Exit Criteria
 - All critical and high-priority test cases pass.
 - Acceptable number of medium and low-priority test cases pass (as per project quality gates).
 - Open bugs are documented and prioritized.

9. Test Cases

Test Area: Shopping Cart
Module: Cart API Endpoints

Test Case ID: CART_UNIT_001
Test Area: Shopping Cart
Test Type: Unit (Conceptual)
Description: Verify the logic for adding a product to an empty cart.
Preconditions: None.
Test Steps:
 - Call the internal function responsible for adding an item to the cart.
 - Provide user ID, product ID, and quantity 1.
 - Simulate initial empty cart state for the user.
Test Data: user_id='test_user', product_id='prod1_mug', quantity=1, initial_cart=[]
Expected Result: The function should return a new cart state for 'test_user' with [{'product_id': 'prod1_mug', 'quantity': 1}].

Test Case ID: CART_UNIT_002
Test Area: Shopping Cart
Test Type: Unit (Conceptual)
Description: Verify the logic for adding a product already in the cart (increasing quantity).
Preconditions: User has the product in their cart.
Test Steps:
 - Call the internal function responsible for adding an item to the cart.
 - Provide user ID, product ID, and quantity 1.
 - Simulate initial cart state for the user with [{"product_id": "prod1_mug", "quantity": 1}].
Test Data: user_id='test_user', product_id='prod1_mug', quantity=1, initial_cart=[{"product_id": "prod1_mug", "quantity": 1}]
Expected Result: The function should return a new cart state for 'test_user' with [{'product_id': 'prod1_mug', 'quantity': 2}].

Test Case ID: CART_UNIT_003
Test Area: Shopping Cart
Test Type: Unit (Conceptual)
Description: Verify the logic for updating the quantity of an item in the cart.
Preconditions: User has the product in their cart.
Test Steps:
 - Call the internal function responsible for updating item quantity.
 - Provide user ID, product ID, and new quantity 3.
 - Simulate initial cart state for the user with [{"product_id": "prod1_mug", "quantity": 1}].
Test Data: user_id='test_user', product_id='prod1_mug', new_quantity=3, initial_cart=[{"product_id": "prod1_mug", "quantity": 1}]
Expected Result: The function should return a new cart state for 'test_user' with [{'product_id': 'prod1_mug', 'quantity': 3}].

Test Case ID: CART_UNIT_004
Test Area: Shopping Cart
Test Type: Unit (Conceptual)
Description: Verify the logic for removing an item from the cart by setting quantity to 0.
Preconditions: User has the product in their cart.
Test Steps:
 - Call the internal function responsible for updating item quantity.
 - Provide user ID, product ID, and new quantity 0.
 - Simulate initial cart state for the user with [{"product_id": "prod1_mug", "quantity": 1}].
Test Data: user_id='test_user', product_id='prod1_mug', new_quantity=0, initial_cart=[{"product_id": "prod1_mug", "quantity": 1}]
Expected Result: The function should return a new empty cart state for 'test_user'.

Test Case ID: CART_INT_001
Test Area: Shopping Cart
Test Type: Integration
Description: Verify GET /api/cart returns correct items for a logged-in user.
Preconditions: User 'user1_cust' is logged in and has items in carts_db.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send GET request to /api/cart with the token in Authorization header.
Test Data: User ID 'user1_cust', products_db and carts_db state.
Expected Result: API returns 200 OK. Response body contains a list of items matching the 'user1_cust' entry in carts_db, including product details like title, price, quantity, and image_url.

Test Case ID: CART_INT_002
Test Area: Shopping Cart
Test Type: Integration
Description: Verify POST /api/cart adds a new product to an empty cart.
Preconditions: User 'user5_cust' is logged in and has an empty cart in carts_db. Product 'prod3_birdhouse' exists and is active with quantity > 0.
Test Steps:
 - Obtain JWT token for 'user5_cust'.
 - Send POST request to /api/cart with {'product_id': 'prod3_birdhouse', 'quantity': 1}.
 - Verify carts_db state for 'user5_cust'.
Test Data: User ID 'user5_cust', product ID 'prod3_birdhouse', quantity 1.
Expected Result: API returns 200 OK. carts_db['user5_cust'] is updated to [{'product_id': 'prod3_birdhouse', 'quantity': 1}].

Test Case ID: CART_INT_003
Test Area: Shopping Cart
Test Type: Integration
Description: Verify POST /api/cart updates quantity if product is already in cart.
Preconditions: User 'user1_cust' is logged in and has 'prod1_mug' in cart with quantity 1. Product 'prod1_mug' is active with quantity > 1.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send POST request to /api/cart with {'product_id': 'prod1_mug', 'quantity': 1}.
 - Verify carts_db state for 'user1_cust'.
Test Data: User ID 'user1_cust', product ID 'prod1_mug', quantity 1. Initial carts_db['user1_cust'] = [{'product_id': 'prod1_mug', 'quantity': 1}, {'product_id': 'prod2_scarf', 'quantity': 2}].
Expected Result: API returns 200 OK. carts_db['user1_cust'] is updated to [{'product_id': 'prod1_mug', 'quantity': 2}, {'product_id': 'prod2_scarf', 'quantity': 2}].

Test Case ID: CART_INT_004
Test Area: Shopping Cart
Test Type: Integration
Description: Verify POST /api/cart fails when adding more than available stock.
Preconditions: User 'user1_cust' is logged in. Product 'prod2_scarf' is active with quantity 8. User has 'prod2_scarf' in cart with quantity 7.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send POST request to /api/cart with {'product_id': 'prod2_scarf', 'quantity': 2}.
Test Data: User ID 'user1_cust', product ID 'prod2_scarf', quantity 2. Initial carts_db['user1_cust'] contains prod2_scarf with quantity 7.
Expected Result: API returns 400 Bad Request with an appropriate error message ("Insufficient stock..."). carts_db state remains unchanged.

Test Case ID: CART_INT_005
Test Area: Shopping Cart
Test Type: Integration
Description: Verify PUT /api/cart/{product_id} updates the quantity of an item.
Preconditions: User 'user1_cust' is logged in. Product 'prod1_mug' is active with quantity > 2. User has 'prod1_mug' in cart with quantity 1.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send PUT request to /api/cart/prod1_mug with {'quantity': 2}.
 - Verify carts_db state for 'user1_cust'.
Test Data: User ID 'user1_cust', product ID 'prod1_mug', new quantity 2. Initial carts_db['user1_cust'] contains prod1_mug with quantity 1.
Expected Result: API returns 200 OK. carts_db['user1_cust'] is updated so prod1_mug has quantity 2.

Test Case ID: CART_INT_006
Test Area: Shopping Cart
Test Type: Integration
Description: Verify PUT /api/cart/{product_id} removes the item when quantity is 0.
Preconditions: User 'user1_cust' is logged in. User has 'prod1_mug' in cart with quantity 1 and 'prod2_scarf' with quantity 2.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send PUT request to /api/cart/prod1_mug with {'quantity': 0}.
 - Verify carts_db state for 'user1_cust'.
Test Data: User ID 'user1_cust', product ID 'prod1_mug', new quantity 0. Initial carts_db['user1_cust'] = [{'product_id': 'prod1_mug', 'quantity': 1}, {'product_id': 'prod2_scarf', 'quantity': 2}].
Expected Result: API returns 200 OK. carts_db['user1_cust'] is updated to [{'product_id': 'prod2_scarf', 'quantity': 2}].

Test Case ID: CART_INT_007
Test Area: Shopping Cart
Test Type: Integration
Description: Verify DELETE /api/cart/{product_id} removes an item from the cart.
Preconditions: User 'user1_cust' is logged in. User has 'prod1_mug' and 'prod2_scarf' in cart.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send DELETE request to /api/cart/prod1_mug.
 - Verify carts_db state for 'user1_cust'.
Test Data: User ID 'user1_cust', product ID 'prod1_mug'. Initial carts_db['user1_cust'] = [{'product_id': 'prod1_mug', 'quantity': 1}, {'product_id': 'prod2_scarf', 'quantity': 2}].
Expected Result: API returns 200 OK. carts_db['user1_cust'] is updated to [{'product_id': 'prod2_scarf', 'quantity': 2}].

Test Case ID: CART_INT_008
Test Area: Shopping Cart
Test Type: Integration
Description: Verify DELETE /api/cart/{product_id} correctly removes the user's entry if it's the last item.
Preconditions: User 'user5_cust' is logged in and has 'prod3_birdhouse' with quantity 1 in cart.
Test Steps:
 - Obtain JWT token for 'user5_cust'.
 - Send DELETE request to /api/cart/prod3_birdhouse.
 - Verify carts_db state.
Test Data: User ID 'user5_cust', product ID 'prod3_birdhouse'. Initial carts_db['user5_cust'] = [{'product_id': 'prod3_birdhouse', 'quantity': 1}].
Expected Result: API returns 200 OK. The 'user5_cust' key is removed from carts_db.

Test Case ID: CART_INT_009
Test Area: Shopping Cart
Test Type: Integration
Description: Verify Cart API endpoints return 401 Unauthorized if no token is provided.
Preconditions: None.
Test Steps:
 - Attempt GET /api/cart without Authorization header.
 - Attempt POST /api/cart without Authorization header.
 - Attempt PUT /api/cart/some_id without Authorization header.
 - Attempt DELETE /api/cart/some_id without Authorization header.
Test Data: N/A
Expected Result: All requests return 401 Unauthorized.

Test Area: Order Creation & Checkout
Module: Checkout API Endpoints

Test Case ID: ORD_INT_001
Test Area: Order Creation
Test Type: Integration
Description: Verify POST /api/checkout/create-order successfully creates an order from the cart.
Preconditions: User 'user1_cust' is logged in and has items in carts_db. All products in the cart are active and in stock.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send POST request to /api/checkout/create-order with {'shipping_address': 'New Shipping Address'}.
 - Verify orders_db contains a new order for 'user1_cust'.
 - Verify carts_db for 'user1_cust' is empty.
 - Verify products_db quantities are updated (decremented) for purchased items.
Test Data: User ID 'user1_cust', shipping_address 'New Shipping Address'. Initial carts_db['user1_cust'] = [{'product_id': 'prod1_mug', 'quantity': 1}, {'product_id': 'prod2_scarf', 'quantity': 2}]. Initial products_db quantities for prod1_mug and prod2_scarf.
Expected Result: API returns 201 Created with order details (order_id, total_amount). orders_db contains a new order with status 'pending_payment' and payment_status 'pending'. carts_db['user1_cust'] is removed or empty. product quantities in products_db are reduced by the ordered quantities.

Test Case ID: ORD_INT_002
Test Area: Order Creation
Test Type: Integration
Description: Verify POST /api/checkout/create-order uses profile shipping address if none provided.
Preconditions: User 'user1_cust' is logged in and has items in carts_db. User profile includes a shipping_address.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send POST request to /api/checkout/create-order with an empty body {}.
 - Verify orders_db contains a new order using the address from 'user1_cust' profile.
Test Data: User ID 'user1_cust'. Initial carts_db['user1_cust'] is not empty. users_db['user1_cust']['profile']['shipping_address'] is set.
Expected Result: API returns 201 Created. The new order in orders_db has the shipping_address from user1_cust's profile.

Test Case ID: ORD_INT_003
Test Area: Order Creation
Test Type: Integration
Description: Verify POST /api/checkout/create-order fails if cart is empty.
Preconditions: User 'user5_cust' is logged in and carts_db['user5_cust'] does not exist or is empty.
Test Steps:
 - Obtain JWT token for 'user5_cust'.
 - Send POST request to /api/checkout/create-order with {'shipping_address': 'Some Address'}.
Test Data: User ID 'user5_cust'. carts_db for user5_cust is empty.
Expected Result: API returns 400 Bad Request with message "Cart is empty". No new order is created.

Test Case ID: ORD_INT_004
Test Area: Order Creation
Test Type: Integration
Description: Verify POST /api/checkout/create-order fails if product is inactive.
Preconditions: User 'user1_cust' is logged in. carts_db['user1_cust'] contains 'prod5_inactive'.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send POST request to /api/checkout/create-order with {'shipping_address': 'Some Address'}.
Test Data: User ID 'user1_cust'. carts_db['user1_cust'] contains 'prod5_inactive'. products_db['prod5_inactive']['status'] is 'inactive'.
Expected Result: API returns 400 Bad Request with message mentioning the product is not available. No new order is created. carts_db and products_db are unchanged.

Test Case ID: ORD_INT_005
Test Area: Order Creation
Test Type: Integration
Description: Verify POST /api/checkout/create-order fails due to insufficient stock.
Preconditions: User 'user1_cust' is logged in. carts_db['user1_cust'] contains 'prod3_birdhouse' with quantity 10. products_db['prod3_birdhouse']['quantity'] is 5.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send POST request to /api/checkout/create-order with {'shipping_address': 'Some Address'}.
Test Data: User ID 'user1_cust'. carts_db['user1_cust'] contains prod3_birdhouse with quantity 10. products_db['prod3_birdhouse']['quantity'] is 5.
Expected Result: API returns 400 Bad Request with message mentioning insufficient stock. No new order is created. carts_db and products_db are unchanged.

Test Case ID: PAY_INT_001
Test Area: Payment Initiation
Test Type: Integration
Description: Verify POST /api/checkout/initiate-payment successfully simulates payment initiation.
Preconditions: User 'user1_cust' is logged in. An order exists in orders_db for 'user1_cust' with status 'pending_payment'.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Identify a pending order ID for 'user1_cust' (e.g., 'order_jkl').
 - Send POST request to /api/checkout/initiate-payment with {'order_id': 'order_jkl'}.
 - Verify the order in orders_db is updated with a simulated 'payment_intent_id'.
Test Data: User ID 'user1_cust', Order ID 'order_jkl'.
Expected Result: API returns 200 OK with simulated 'payment_intent_id' and 'client_secret'. The order 'order_jkl' in orders_db has a non-None 'payment_intent_id'.

Test Case ID: PAY_INT_002
Test Area: Payment Initiation
Test Type: Integration
Description: Verify POST /api/checkout/initiate-payment fails for an order not owned by the user.
Preconditions: User 'user1_cust' is logged in. Order 'order_def' exists but is owned by 'user5_cust'.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send POST request to /api/checkout/initiate-payment with {'order_id': 'order_def'}.
Test Data: User ID 'user1_cust', Order ID 'order_def'.
Expected Result: API returns 404 Not Found (or 403 Forbidden depending on exact logic) with an appropriate error message. The order 'order_def' in orders_db is unchanged.

Test Case ID: PAY_INT_003
Test Area: Payment Initiation
Test Type: Integration
Description: Verify POST /api/checkout/initiate-payment fails for an order already paid.
Preconditions: User 'user1_cust' is logged in. Order 'order_abc' exists for 'user1_cust' with payment_status 'paid'.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send POST request to /api/checkout/initiate-payment with {'order_id': 'order_abc'}.
Test Data: User ID 'user1_cust', Order ID 'order_abc'.
Expected Result: API returns 400 Bad Request with message "Payment for this order is already processed...". The order 'order_abc' in orders_db is unchanged.

Test Area: Payment Webhook Simulation
Module: payment-webhook Endpoint

Test Case ID: WH_INT_001
Test Area: Payment Webhook
Test Type: Integration
Description: Verify POST /api/checkout/payment-webhook successfully processes a simulated 'payment_intent.succeeded' event.
Preconditions: Order 'order_jkl' exists in orders_db with status 'pending_payment' and payment_status 'pending'.
Test Steps:
 - Send POST request to /api/checkout/payment-webhook with a simulated JSON payload indicating success for 'order_jkl' (e.g., {'type': 'payment_intent.succeeded', 'data': {'object': {'id': 'sim_pi_for_jkl', 'metadata': {'order_id': 'order_jkl'}} } }).
 - Verify the status and payment_status of order 'order_jkl' in orders_db are updated.
 - Verify a simulated email notification is triggered for the customer.
Test Data: Simulated webhook payload for order_jkl.
Expected Result: API returns 200 OK. Order 'order_jkl' in orders_db has status 'processing' and payment_status 'paid'. A message indicating email simulation for 'customer2@example.com' is printed to console.

Test Case ID: WH_INT_002
Test Area: Payment Webhook
Test Type: Integration
Description: Verify POST /api/checkout/payment-webhook ignores events that are not 'payment_intent.succeeded'.
Preconditions: Order 'order_jkl' exists in orders_db with status 'pending_payment'.
Test Steps:
 - Send POST request to /api/checkout/payment-webhook with a simulated JSON payload indicating a different event type (e.g., {'type': 'payment_intent.payment_failed', 'data': {'object': {'metadata': {'order_id': 'order_jkl'}}}}).
Test Data: Simulated webhook payload with type 'payment_intent.payment_failed'.
Expected Result: API returns 200 OK (indicating webhook received) and message "Event type ignored". Order 'order_jkl' in orders_db is unchanged.

Test Case ID: WH_INT_003
Test Area: Payment Webhook
Test Type: Integration
Description: Verify POST /api/checkout/payment-webhook handles processing an already paid order idempotently.
Preconditions: Order 'order_abc' exists in orders_db with status 'processing' and payment_status 'paid'.
Test Steps:
 - Send POST request to /api/checkout/payment-webhook with a simulated JSON payload indicating success for 'order_abc'.
Test Data: Simulated webhook payload for order_abc.
Expected Result: API returns 200 OK with message "Order already paid". Order 'order_abc' in orders_db is unchanged.

Test Area: Customer Order History
Module: Customer Orders API Endpoints

Test Case ID: CUSTORD_INT_001
Test Area: Customer Order History
Test Type: Integration
Description: Verify GET /api/customer/orders returns list of orders for the logged-in customer.
Preconditions: User 'user1_cust' is logged in. Orders 'order_abc' and 'order_ghi' exist and belong to 'user1_cust'.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send GET request to /api/customer/orders.
Test Data: User ID 'user1_cust'. orders_db state.
Expected Result: API returns 200 OK. Response body is a list containing data for 'order_abc' and 'order_ghi', sorted by date (newest first).

Test Case ID: CUSTORD_INT_002
Test Area: Customer Order History
Test Type: Integration
Description: Verify GET /api/customer/orders returns empty list for a customer with no orders.
Preconditions: User 'user5_cust' is logged in. After potentially testing order creation, ensure they have no orders or use a new test user.
Test Steps:
 - Obtain JWT token for 'user5_cust'.
 - Send GET request to /api/customer/orders.
Test Data: User ID 'user5_cust'. orders_db contains no orders for this user.
Expected Result: API returns 200 OK. Response body is an empty list [].

Test Case ID: CUSTORD_INT_003
Test Area: Customer Order History
Test Type: Integration
Description: Verify GET /api/customer/orders/{order_id} returns details for a specific order owned by the customer.
Preconditions: User 'user1_cust' is logged in. Order 'order_abc' exists and belongs to 'user1_cust'.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send GET request to /api/customer/orders/order_abc.
Test Data: User ID 'user1_cust', Order ID 'order_abc'. products_db state.
Expected Result: API returns 200 OK. Response body contains full details for order 'order_abc', including detailed items with product information.

Test Case ID: CUSTORD_INT_004
Test Area: Customer Order History
Test Type: Integration
Description: Verify GET /api/customer/orders/{order_id} returns 404 Not Found for an order not owned by the customer.
Preconditions: User 'user1_cust' is logged in. Order 'order_def' exists but belongs to 'user5_cust'.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send GET request to /api/customer/orders/order_def.
Test Data: User ID 'user1_cust', Order ID 'order_def'.
Expected Result: API returns 404 Not Found with an appropriate error message.

Test Case ID: CUSTORD_INT_005
Test Area: Customer Order History
Test Type: Integration
Description: Verify GET /api/customer/orders/{order_id} returns 404 Not Found for a non-existent order ID.
Preconditions: User 'user1_cust' is logged in.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send GET request to /api/customer/orders/non_existent_order.
Test Data: User ID 'user1_cust', Order ID 'non_existent_order'.
Expected Result: API returns 404 Not Found with an appropriate error message.

Test Area: Product Reviews & Ratings
Module: Reviews API Endpoints

Test Case ID: REV_INT_001
Test Area: Product Reviews
Test Type: Integration
Description: Verify GET /api/products/{product_id}/reviews returns reviews for a product.
Preconditions: Product 'prod1_mug' exists and is active. Reviews 'review1' exists for 'prod1_mug'.
Test Steps:
 - Send GET request to /api/products/prod1_mug/reviews.
Test Data: Product ID 'prod1_mug'. reviews_db and users_db state.
Expected Result: API returns 200 OK. Response body is a list containing details for 'review1', including customer name.

Test Case ID: REV_INT_002
Test Area: Product Reviews
Test Type: Integration
Description: Verify GET /api/products/{product_id}/reviews returns empty list for a product with no reviews.
Preconditions: Product 'prod2_scarf' exists and is active and has no reviews in reviews_db.
Test Steps:
 - Send GET request to /api/products/prod2_scarf/reviews.
Test Data: Product ID 'prod2_scarf'. reviews_db state.
Expected Result: API returns 200 OK. Response body is an empty list [].

Test Case ID: REV_INT_003
Test Area: Product Reviews
Test Type: Integration
Description: Verify GET /api/products/{product_id}/reviews returns 404 for a non-existent or inactive product.
Preconditions: Product 'non_existent_prod' does not exist. Product 'prod5_inactive' exists but is inactive.
Test Steps:
 - Send GET request to /api/products/non_existent_prod/reviews.
 - Send GET request to /api/products/prod5_inactive/reviews.
Test Data: Product IDs 'non_existent_prod', 'prod5_inactive'.
Expected Result: Both requests return 404 Not Found.

Test Case ID: REV_INT_004
Test Area: Product Reviews
Test Type: Integration
Description: Verify POST /api/products/{product_id}/reviews successfully submits a review for a purchased product.
Preconditions: User 'user1_cust' is logged in. Order 'order_abc' exists for 'user1_cust' with status 'processing' (or later) and contains 'prod1_mug'. Product 'prod1_mug' is active.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send POST request to /api/products/prod1_mug/reviews with {'rating': 5, 'comment': 'Excellent!'}.
 - Verify reviews_db contains a new review entry.
Test Data: User ID 'user1_cust', Product ID 'prod1_mug', rating 5, comment 'Excellent!'. orders_db state showing user1_cust purchased prod1_mug. products_db state.
Expected Result: API returns 201 Created with the new review ID. reviews_db contains a new entry for prod1_mug by user1_cust with the provided rating and comment.

Test Case ID: REV_INT_005
Test Area: Product Reviews
Test Type: Integration
Description: Verify POST /api/products/{product_id}/reviews fails for a product not purchased by the user.
Preconditions: User 'user5_cust' is logged in. Order 'order_abc' exists for 'user1_cust' and contains 'prod1_mug'. User 'user5_cust' has not purchased 'prod1_mug'. Product 'prod1_mug' is active.
Test Steps:
 - Obtain JWT token for 'user5_cust'.
 - Send POST request to /api/products/prod1_mug/reviews with {'rating': 3, 'comment': 'Seems okay'}.
Test Data: User ID 'user5_cust', Product ID 'prod1_mug', rating 3, comment 'Seems okay'. orders_db state.
Expected Result: API returns 403 Forbidden with message "You can only review products you have purchased". reviews_db is unchanged.

Test Case ID: REV_INT_006
Test Area: Product Reviews
Test Type: Integration
Description: Verify POST /api/products/{product_id}/reviews fails with invalid rating (out of range).
Preconditions: User 'user1_cust' is logged in and has purchased 'prod1_mug'. Product 'prod1_mug' is active.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send POST request to /api/products/prod1_mug/reviews with {'rating': 6, 'comment': 'Bad rating'}.
 - Send POST request to /api/products/prod1_mug/reviews with {'rating': 0, 'comment': 'Bad rating'}.
Test Data: User ID 'user1_cust', Product ID 'prod1_mug', ratings 6 and 0.
Expected Result: Both requests return 400 Bad Request with message "Rating must be an integer between 1 and 5". reviews_db is unchanged.

Test Case ID: REV_INT_007
Test Area: Product Reviews
Test Type: Integration
Description: Verify POST /api/products/{product_id}/reviews fails with invalid rating (not integer).
Preconditions: User 'user1_cust' is logged in and has purchased 'prod1_mug'. Product 'prod1_mug' is active.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send POST request to /api/products/prod1_mug/reviews with {'rating': 'abc', 'comment': 'Bad rating'}.
 - Send POST request to /api/products/prod1_mug/reviews with {'rating': 4.5, 'comment': 'Bad rating'}.
Test Data: User ID 'user1_cust', Product ID 'prod1_mug', ratings 'abc' and 4.5.
Expected Result: Both requests return 400 Bad Request with message "Rating must be an integer between 1 and 5". reviews_db is unchanged.

Test Case ID: REV_INT_008
Test Area: Product Reviews
Test Type: Integration
Description: Verify POST /api/products/{product_id}/reviews succeeds with empty comment.
Preconditions: User 'user1_cust' is logged in and has purchased 'prod1_mug'. Product 'prod1_mug' is active.
Test Steps:
 - Obtain JWT token for 'user1_cust'.
 - Send POST request to /api/products/prod1_mug/reviews with {'rating': 4, 'comment': ''}.
Test Data: User ID 'user1_cust', Product ID 'prod1_mug', rating 4, comment ''.
Expected Result: API returns 201 Created. reviews_db contains a new entry with the provided rating and an empty comment string.

Test Area: Seller Order Management
Module: Seller Orders API Endpoints

Test Case ID: SELLORD_INT_001
Test Area: Seller Order Management
Test Type: Integration
Description: Verify GET /api/seller/orders returns list of orders containing the seller's products.
Preconditions: User 'user2_seller' is logged in and approved. Orders 'order_abc' and 'order_ghi' contain products from 'user2_seller'. Order 'order_def' does not.
Test Steps:
 - Obtain JWT token for 'user2_seller'.
 - Send GET request to /api/seller/orders.
Test Data: User ID 'user2_seller'. orders_db and products_db states.
Expected Result: API returns 200 OK. Response body is a list containing overview data for 'order_abc' and 'order_ghi', sorted by date (newest first). It should NOT include 'order_def'.

Test Case ID: SELLORD_INT_002
Test Area: Seller Order Management
Test Type: Integration
Description: Verify GET /api/seller/orders returns empty list for a seller with no orders containing their products.
Preconditions: User 'user4_seller' is logged in and approved. All existing orders in orders_db contain products only from 'user2_seller'.
Test Steps:
 - Obtain JWT token for 'user4_seller'.
 - Send GET request to /api/seller/orders.
Test Data: User ID 'user4_seller'. orders_db and products_db states where no order contains user4_seller's products.
Expected Result: API returns 200 OK. Response body is an empty list [].

Test Case ID: SELLORD_INT_003
Test Area: Seller Order Management
Test Type: Integration
Description: Verify GET /api/seller/orders/{order_id} returns details for an order containing the seller's products.
Preconditions: User 'user2_seller' is logged in and approved. Order 'order_abc' exists and contains products from 'user2_seller'.
Test Steps:
 - Obtain JWT token for 'user2_seller'.
 - Send GET request to /api/seller/orders/order_abc.
Test Data: User ID 'user2_seller', Order ID 'order_abc'. orders_db, products_db, users_db states.
Expected Result: API returns 200 OK. Response body contains details for order 'order_abc', including customer shipping info and only the items from 'user2_seller'.

Test Case ID: SELLORD_INT_004
Test Area: Seller Order Management
Test Type: Integration
Description: Verify GET /api/seller/orders/{order_id} returns 403 Forbidden for an order that does NOT contain the seller's products.
Preconditions: User 'user2_seller' is logged in and approved. Order 'order_def' exists but contains products only from 'user4_seller'.
Test Steps:
 - Obtain JWT token for 'user2_seller'.
 - Send GET request to /api/seller/orders/order_def.
Test Data: User ID 'user2_seller', Order ID 'order_def'. orders_db, products_db states.
Expected Result: API returns 403 Forbidden with message "You do not have permission...".

Test Case ID: SELLORD_INT_005
Test Area: Seller Order Management
Test Type: Integration
Description: Verify GET /api/seller/orders/{order_id} returns 404 Not Found for a non-existent order ID.
Preconditions: User 'user2_seller' is logged in and approved.
Test Steps:
 - Obtain JWT token for 'user2_seller'.
 - Send GET request to /api/seller/orders/non_existent_order.
Test Data: User ID 'user2_seller', Order ID 'non_existent_order'.
Expected Result: API returns 404 Not Found.

Test Case ID: SELLORD_INT_006
Test Area: Seller Order Management
Test Type: Integration
Description: Verify PUT /api/seller/orders/{order_id}/status successfully updates status to 'shipped' and adds tracking.
Preconditions: User 'user2_seller' is logged in and approved. Order 'order_ghi' exists and contains products from 'user2_seller' and is in 'processing' status.
Test Steps:
 - Obtain JWT token for 'user2_seller'.
 - Send PUT request to /api/seller/orders/order_ghi/status with {'status': 'shipped', 'tracking_number': 'SELLERTRACK123'}.
 - Verify the status and tracking_number of order 'order_ghi' in orders_db are updated.
 - Verify a simulated email notification is triggered for the customer.
Test Data: User ID 'user2_seller', Order ID 'order_ghi'. New status 'shipped', tracking_number 'SELLERTRACK123'. Initial orders_db state for order_ghi.
Expected Result: API returns 200 OK. Order 'order_ghi' in orders_db has status 'shipped' and tracking_number 'SELLERTRACK123'. A message indicating email simulation for 'customer1@example.com' with shipping details is printed to console.

Test Case ID: SELLORD_INT_007
Test Area: Seller Order Management
Test Type: Integration
Description: Verify PUT /api/seller/orders/{order_id}/status fails if status is not 'shipped'.
Preconditions: User 'user2_seller' is logged in and approved. Order 'order_ghi' exists and is in 'processing' status.
Test Steps:
 - Obtain JWT token for 'user2_seller'.
 - Send PUT request to /api/seller/orders/order_ghi/status with {'status': 'delivered', 'tracking_number': 'SELLERTRACK456'}.
Test Data: User ID 'user2_seller', Order ID 'order_ghi'. New status 'delivered'.
Expected Result: API returns 400 Bad Request with message about invalid status update. Order 'order_ghi' is unchanged.

Test Case ID: SELLORD_INT_008
Test Area: Seller Order Management
Test Type: Integration
Description: Verify PUT /api/seller/orders/{order_id}/status fails if tracking number is missing when setting to 'shipped'.
Preconditions: User 'user2_seller' is logged in and approved. Order 'order_ghi' exists and is in 'processing' status.
Test Steps:
 - Obtain JWT token for 'user2_seller'.
 - Send PUT request to /api/seller/orders/order_ghi/status with {'status': 'shipped'}.
Test Data: User ID 'user2_seller', Order ID 'order_ghi'. New status 'shipped', missing tracking_number.
Expected Result: API returns 400 Bad Request with message about tracking number being required. Order 'order_ghi' is unchanged.

Test Case ID: SELLORD_INT_009
Test Area: Seller Order Management
Test Type: Integration
Description: Verify PUT /api/seller/orders/{order_id}/status fails for an order that does NOT contain the seller's products.
Preconditions: User 'user2_seller' is logged in and approved. Order 'order_def' exists but contains products only from 'user4_seller' and is in 'shipped' status.
Test Steps:
 - Obtain JWT token for 'user2_seller'.
 - Send PUT request to /api/seller/orders/order_def/status with {'status': 'shipped', 'tracking_number': 'FAKETRACK'}.
Test Data: User ID 'user2_seller', Order ID 'order_def'. New status 'shipped'.
Expected Result: API returns 403 Forbidden with message "You do not have permission...". Order 'order_def' is unchanged.

Test Area: Admin Order Management
Module: Admin Orders API Endpoints

Test Case ID: ADMINORD_INT_001
Test Area: Admin Order Management
Test Type: Integration
Description: Verify GET /api/admin/orders returns list of all orders.
Preconditions: User 'user3_admin' is logged in. Orders 'order_abc', 'order_def', 'order_ghi', 'order_jkl' exist.
Test Steps:
 - Obtain JWT token for 'user3_admin'.
 - Send GET request to /api/admin/orders.
Test Data: User ID 'user3_admin'. orders_db, users_db, products_db states.
Expected Result: API returns 200 OK. Response body is a list containing overview data for all orders in orders_db, including customer and item count, sorted by date.

Test Case ID: ADMINORD_INT_002
Test Area: Admin Order Management
Test Type: Integration
Description: Verify GET /api/admin/orders/{order_id} returns full details for any order.
Preconditions: User 'user3_admin' is logged in. Order 'order_ghi' exists.
Test Steps:
 - Obtain JWT token for 'user3_admin'.
 - Send GET request to /api/admin/orders/order_ghi.
Test Data: User ID 'user3_admin', Order ID 'order_ghi'. orders_db, users_db, products_db states.
Expected Result: API returns 200 OK. Response body contains full details for order 'order_ghi', including customer info (including email), shipping address, overall status, payment status, tracking, and details for ALL items in the order, including seller info for each item.

Test Case ID: ADMINORD_INT_003
Test Area: Admin Order Management
Test Type: Integration
Description: Verify GET /api/admin/orders/{order_id} returns 404 Not Found for a non-existent order ID.
Preconditions: User 'user3_admin' is logged in.
Test Steps:
 - Obtain JWT token for 'user3_admin'.
 - Send GET request to /api/admin/orders/non_existent_order_admin.
Test Data: User ID 'user3_admin', Order ID 'non_existent_order_admin'.
Expected Result: API returns 404 Not Found.

Test Case ID: ADMINORD_INT_004
Test Area: Admin Order Management
Test Type: Integration
Description: Verify PUT /api/admin/orders/{order_id}/status updates order status, payment status, and tracking.
Preconditions: User 'user3_admin' is logged in. Order 'order_ghi' exists in 'processing' status, 'paid' payment status, no tracking.
Test Steps:
 - Obtain JWT token for 'user3_admin'.
 - Send PUT request to /api/admin/orders/order_ghi/status with {'status': 'delivered', 'payment_status': 'paid', 'tracking_number': 'ADMINTRACK456'}.
 - Verify status, payment_status, and tracking_number are updated in orders_db.
 - Verify a simulated email notification for customer is triggered due to status change.
Test Data: User ID 'user3_admin', Order ID 'order_ghi'. New status 'delivered', payment_status 'paid', tracking_number 'ADMINTRACK456'. Initial orders_db state for order_ghi.
Expected Result: API returns 200 OK. Order 'order_ghi' in orders_db has status 'delivered', payment_status 'paid', tracking_number 'ADMINTRACK456'. A message indicating email simulation for 'customer1@example.com' is printed.

Test Case ID: ADMINORD_INT_005
Test Area: Admin Order Management
Test Type: Integration
Description: Verify PUT /api/admin/orders/{order_id}/status allows setting tracking_number to None.
Preconditions: User 'user3_admin' is logged in. Order 'order_def' exists with status 'shipped' and tracking 'TRACKXYZ789'.
Test Steps:
 - Obtain JWT token for 'user3_admin'.
 - Send PUT request to /api/admin/orders/order_def/status with {'status': 'shipped', 'tracking_number': None}.
 - Verify tracking_number is updated to None in orders_db.
Test Data: User ID 'user3_admin', Order ID 'order_def'. New status 'shipped', tracking_number None. Initial orders_db state for order_def.
Expected Result: API returns 200 OK. Order 'order_def' in orders_db has status 'shipped' and tracking_number is None. No email is triggered as status didn't change significantly.

Test Case ID: ADMINORD_INT_006
Test Area: Admin Order Management
Test Type: Integration
Description: Verify PUT /api/admin/orders/{order_id}/status fails for invalid status.
Preconditions: User 'user3_admin' is logged in. Order 'order_ghi' exists.
Test Steps:
 - Obtain JWT token for 'user3_admin'.
 - Send PUT request to /api/admin/orders/order_ghi/status with {'status': 'fake_status'}.
Test Data: User ID 'user3_admin', Order ID 'order_ghi'. New status 'fake_status'.
Expected Result: API returns 400 Bad Request with message about invalid status. Order 'order_ghi' is unchanged.

Test Case ID: ADMINORD_INT_007
Test Area: Admin Order Management
Test Type: Integration
Description: Verify Admin Order endpoints return 403 Forbidden if not an admin.
Preconditions: User 'user1_cust' (customer) and 'user2_seller' (seller) are logged in.
Test Steps:
 - Obtain JWT token for 'user1_cust'. Send GET /api/admin/orders with token. Send GET /api/admin/orders/order_abc with token. Send PUT /api/admin/orders/order_abc/status with token.
 - Obtain JWT token for 'user2_seller'. Send GET /api/admin/orders with token. Send GET /api/admin/orders/order_abc with token. Send PUT /api/admin/orders/order_abc/status with token.
Test Data: User IDs 'user1_cust', 'user2_seller'. Order ID 'order_abc'.
Expected Result: All requests return 403 Forbidden.

Test Area: End-to-End Flows (Simulated Frontend Interaction)
Module: Multiple Endpoints

Test Case ID: E2E_001
Test Area: Customer Purchase Flow
Test Type: End-to-End
Description: Simulate a customer adding items, proceeding to checkout, and completing payment.
Preconditions: Customer user exists and is logged in. Products exist and are in stock. Simulated Payment Webhook endpoint is functional.
Test Steps:
 - Simulate customer adding 'prod1_mug' (qty 1) and 'prod2_scarf' (qty 2) to cart via frontend actions (calls POST /api/cart).
 - Simulate customer viewing cart (calls GET /api/cart) and verifying items.
 - Simulate customer proceeding to checkout and entering shipping address (calls POST /api/checkout/create-order).
 - Simulate customer initiating payment (calls POST /api/checkout/initiate-payment).
 - Manually or programmatically simulate the payment gateway sending a success webhook (calls POST /api/checkout/payment-webhook).
 - Simulate customer viewing their order history (calls GET /api/customer/orders) and verifying the new order status.
 - Simulate customer viewing order details (calls GET /api/customer/orders/{order_id}) and verifying details.
Test Data: Customer user ID, product IDs, quantities, shipping address.
Expected Result:
 - Cart endpoints return 200, cart state updates correctly.
 - Create Order returns 201, a new order appears in orders_db (pending_payment), cart is cleared, product stock is decremented.
 - Initiate Payment returns 200 with simulated payment details, order is updated with payment_intent_id.
 - Webhook returns 200, order status in orders_db updates to 'processing' and payment_status to 'paid'. Customer receives simulated confirmation email.
 - Customer Order History shows the new order with updated status. Order Details show correct items, price, status, etc.

Test Case ID: E2E_002
Test Area: Seller Order Fulfillment Flow
Test Type: End-to-End
Description: Simulate a seller logging in, viewing orders, and marking an order as shipped.
Preconditions: Seller user exists and is logged in and approved. An order containing the seller's product exists and is in 'processing' status.
Test Steps:
 - Simulate seller logging in (calls Engineer 1's /api/login).
 - Simulate seller navigating to their orders page (calls GET /api/seller/orders).
 - Simulate seller viewing details of a specific order (calls GET /api/seller/orders/{order_id}).
 - Simulate seller marking the order as shipped and entering tracking (calls PUT /api/seller/orders/{order_id}/status).
 - Verify the order status and tracking_number in orders_db are updated.
 - Verify the customer receives a simulated shipping notification email.
Test Data: Seller user ID, order ID containing seller's products, tracking number.
Expected Result:
 - Login succeeds, token is received.
 - Seller Orders list shows the relevant order.
 - Seller Order Details show correct information for the seller's items and customer shipping address.
 - Update status returns 200. Order in orders_db is updated to 'shipped' with the tracking number. Customer receives simulated shipping email.
 - Seller Orders list and details views now reflect the 'shipped' status and tracking.

Test Case ID: E2E_003
Test Area: Customer Review Flow
Test Type: End-to-End
Description: Simulate a customer who purchased a product leaving a review.
Preconditions: Customer user exists and is logged in. An order for this customer exists with status 'shipped', 'delivered', or 'completed' and contains a specific product.
Test Steps:
 - Simulate customer logging in.
 - Simulate customer navigating to their order history (calls GET /api/customer/orders).
 - Simulate customer viewing details of the order containing the reviewable product (calls GET /api/customer/orders/{order_id}).
 - Simulate customer clicking a link/button to review the specific product (assuming frontend handles navigation and form).
 - Simulate customer submitting the review form (calls POST /api/products/{product_id}/reviews).
 - Simulate customer viewing the product details page (calls GET /api/products/{product_id}) and verifying their review appears in the reviews list (calls GET /api/products/{product_id}/reviews).
Test Data: Customer user ID, order ID, product ID, rating, comment.
Expected Result:
 - Login, order history, and order details calls succeed.
 - Submit review call returns 201 Created. A new review appears in reviews_db associated with the user and product.
 - Product reviews list includes the newly submitted review.

Test Area: Email Notifications
Module: send_email_notification Helper and Triggers

Test Case ID: NOTIF_INT_001
Test Area: Email Notifications
Test Type: Integration
Description: Verify order confirmation email is triggered after successful payment via webhook.
Preconditions: Simulated Payment Webhook endpoint is called with a successful payment event for a pending order. Customer user exists with an email.
Test Steps:
 - Trigger the webhook endpoint with a success payload for order 'order_jkl'.
 - Observe console output for email simulation.
Test Data: Webhook payload for order 'order_jkl'. User 'user5_cust' email.
Expected Result: Console output shows "--- Simulating Email Notification ---" with recipient 'customer2@example.com' and a subject/body indicating order confirmation for 'order_jkl'.

Test Case ID: NOTIF_INT_002
Test Area: Email Notifications
Test Type: Integration
Description: Verify shipping notification email is triggered when seller updates status to 'shipped'.
Preconditions: Seller update status endpoint is called to set status to 'shipped' for an order containing their product. Customer user exists with an email.
Test Steps:
 - Obtain JWT for 'user2_seller'.
 - Call PUT /api/seller/orders/order_ghi/status with {'status': 'shipped', 'tracking_number': 'TRACK123'}.
 - Observe console output for email simulation.
Test Data: User ID 'user2_seller', Order ID 'order_ghi', status 'shipped', tracking 'TRACK123'. User 'user1_cust' email.
Expected Result: API returns 200 OK. Console output shows "--- Simulating Email Notification ---" with recipient 'customer1@example.com' and a subject/body indicating shipment for 'order_ghi' from 'Seller Shop A' including tracking number and item list.

Test Case ID: NOTIF_INT_003
Test Area: Email Notifications
Test Type: Integration
Description: Verify notification email is triggered when admin updates status to 'cancelled'.
Preconditions: Admin user is logged in. Order 'order_abc' exists. Customer user exists with an email.
Test Steps:
 - Obtain JWT for 'user3_admin'.
 - Call PUT /api/admin/orders/order_abc/status with {'status': 'cancelled'}.
 - Observe console output for email simulation.
Test Data: User ID 'user3_admin', Order ID 'order_abc', status 'cancelled'. User 'user1_cust' email.
Expected Result: API returns 200 OK. Console output shows "--- Simulating Email Notification ---" with recipient 'customer1@example.com' and a subject/body indicating cancellation for 'order_abc'.

--- End of Test Plan ---