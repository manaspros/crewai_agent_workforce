TEST PLAN DOCUMENT: E-commerce Website for Handmade Crafts

1. INTRODUCTION

This test plan outlines the strategy, scope, resources, and schedule for testing the E-commerce Website for Handmade Crafts. The goal is to ensure the platform meets the functional, performance, security, and usability requirements defined in the product specification, covering both frontend and backend components (V1 scope).

2. TESTING OBJECTIVES

- Verify that all key features for buyers, sellers (approved), and admins function correctly according to the product specification.
- Ensure the security of user data and transactions.
- Test the performance and responsiveness of the website under various conditions.
- Validate the usability and user experience across different devices and user roles.
- Confirm reliable communication between frontend and backend components via the API.
- Identify and report defects to ensure product quality before release.

3. TEST TYPES

- Unit Testing: Testing individual components or functions (backend functions, simple frontend JS functions).
- Integration Testing: Testing interactions between integrated components (backend API endpoints interacting with the database, frontend JS logic interacting with DOM/simulated data).
- API Functional Testing: Testing the backend RESTful API endpoints directly using various inputs and verifying outputs and status codes.
- End-to-End Testing: Testing complete user workflows across the integrated frontend and backend (simulated via API or conceptual for the provided basic frontend).
- Functional Testing: Verifying that each feature works as specified (covering UI interactions, data validation, business logic).
- Security Testing: Checking for common vulnerabilities (injection, authentication bypass, authorization issues).
- Performance Testing: Assessing loading times and responsiveness (basic checks within scope).
- Usability Testing: Evaluating ease of use and user experience (basic walkthroughs).

4. TEST ENVIRONMENT

- Frontend: Modern Web Browsers (Chrome, Firefox, Safari, Edge) on Desktop, Tablet, and Mobile viewports.
- Backend: Server environment hosting the Flask application and SQLAlchemy (in-memory SQLite for provided code, but concept is portable to PostgreSQL/MySQL).
- API Testing Tool: Postman, cURL, or similar.
- Data: Test database with sample users (admin, seller, buyer), seller profiles (approved/pending), products (approved/unapproved), addresses, cart items, and orders.

5. TEST DATA

- Buyer user accounts (registered).
- Seller user accounts (registered, some approved, some pending).
- Admin user account.
- Sample product data (various prices, stock levels, images).
- Sample address data for buyers.
- Sample cart data (empty, single item, multiple items, multiple quantities).
- Sample order data (different statuses, tracking numbers).
- Invalid inputs for forms and API requests (invalid email, password, quantities, prices, non-existent IDs, missing required fields).
- Edge cases (zero stock, zero price - if applicable, very long inputs - basic check).

6. ENTRY CRITERIA

- Product specification signed off.
- Development environment stable and deployed.
- All major features included in V1 scope are implemented and available for testing.
- Smoke tests passed on the deployed environment.
- Required test data is available.

7. EXIT CRITERIA

- All critical and high-priority test cases passed.
- All known medium-priority defects reviewed and accepted by stakeholders, or fixed and retested.
- Low-priority defects logged for future sprints.
- Test coverage goals met (e.g., key workflows covered).
- Performance and security checks deemed acceptable for V1.

8. TEST DELIVERABLES

- Test Plan document.
- Test Cases (detailed below).
- Test Data sets (description/scripts).
- Test Execution Reports (including status of test cases).
- Defect Reports (including steps to reproduce, actual vs. expected results).

9. ROLES AND RESPONSIBILITIES

- QA Engineer: Test planning, test case design, test execution, defect reporting and tracking.
- Developer: Fix defects, support test environment setup.
- Product Owner/Stakeholder: Clarify requirements, prioritize defects.

10. RISK ASSESSMENT (BRIEF)

- Delays in development impacting testing schedule.
- Insufficient test data for comprehensive coverage.
- Instability of the test environment.
- Scope creep affecting planned test coverage.
- Security vulnerabilities in payment processing (mitigated by using reputable gateway, though simulation only in code).

11. TEST SCHEDULE (PLACEHOLDER)

- Test Planning & Design: [Start Date] - [End Date]
- Test Environment Setup: [Start Date] - [End Date]
- Test Data Preparation: [Start Date] - [End Date]
- Test Execution Cycles: [Start Date] - [End Date] (Include regression testing)
- Defect Triage & Retesting: Ongoing
- Test Closure: [Date]

12. TEST CASES

This section details individual test cases.

TEST CASE ID: BE_UNIT_AUTH_001
MODULE: Backend User Model
DESCRIPTION: Verify User.set_password hashes the password.
PRECONDITIONS: None.
TEST STEPS:
1. Create a User instance.
2. Call user.set_password('testpassword123').
3. Assert that user.password_hash is not 'testpassword123'.
4. Assert that user.password_hash is not None or empty.
EXPECTED RESULT: The password_hash attribute is populated with a non-empty string different from the input password.
PRIORITY: High
TEST TYPE: Unit
STATUS: Not Executed

TEST CASE ID: BE_UNIT_AUTH_002
MODULE: Backend User Model
DESCRIPTION: Verify User.check_password correctly validates a password against the hash.
PRECONDITIONS: A User instance exists with a password set using set_password.
TEST STEPS:
1. Create a User instance and set password 'testpassword123'.
2. Call user.check_password('testpassword123').
3. Call user.check_password('wrongpassword').
EXPECTED RESULT: Step 2 returns True. Step 3 returns False.
PRIORITY: High
TEST TYPE: Unit
STATUS: Not Executed

TEST CASE ID: BE_INT_DB_001
MODULE: Backend Database Integration
DESCRIPTION: Verify a new User record is successfully inserted into the database.
PRECONDITIONS: Database is accessible.
TEST STEPS:
1. Create a new User object.
2. Add the user to the session.
3. Commit the session.
4. Query the database for the user by email or ID.
5. Assert the user record is found and attributes match.
EXPECTED RESULT: A User record is present in the database after commit.
PRIORITY: High
TEST TYPE: Integration
STATUS: Not Executed

TEST CASE ID: BE_API_AUTH_001
MODULE: Backend API Authentication
DESCRIPTION: Test successful user registration via POST /register.
PRECONDITIONS: Backend server is running.
TEST STEPS:
1. Send a POST request to /register with valid email and password in the body.
2. Check the response status code.
3. Check the response body for success message and user_id.
4. Optionally, query the database directly to confirm user creation with hashed password.
EXPECTED RESULT: Status code 201. Response body indicates success and includes user_id. User record exists in DB with hashed password.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_AUTH_002
MODULE: Backend API Authentication
DESCRIPTION: Test user registration with existing email via POST /register.
PRECONDITIONS: A user with the test email already exists in the database.
TEST STEPS:
1. Send a POST request to /register with the existing email and any password.
2. Check the response status code.
3. Check the response body for an error message indicating email already exists.
EXPECTED RESULT: Status code 409. Response body indicates conflict (email exists).
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_AUTH_003
MODULE: Backend API Authentication
DESCRIPTION: Test user registration with missing required fields via POST /register.
PRECONDITIONS: Backend server is running.
TEST STEPS:
1. Send a POST request to /register with missing email (only password).
2. Check the response status code and body.
3. Send a POST request to /register with missing password (only email).
4. Check the response status code and body.
5. Send a POST request to /register with empty body.
6. Check the response status code and body.
EXPECTED RESULT: Status code 400 for all steps. Response body indicates missing fields.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_AUTH_004
MODULE: Backend API Authentication
DESCRIPTION: Test successful user login via POST /login.
PRECONDITIONS: A registered user exists in the database.
TEST STEPS:
1. Send a POST request to /login with the valid email and password of the existing user.
2. Check the response status code.
3. Check the response body for a token, user_id, and role.
4. Store the received token.
EXPECTED RESULT: Status code 200. Response body contains a non-empty token, user_id, and correct role ('buyer').
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_AUTH_005
MODULE: Backend API Authentication
DESCRIPTION: Test user login with invalid credentials via POST /login.
PRECONDITIONS: Backend server is running.
TEST STEPS:
1. Send a POST request to /login with a valid email but wrong password.
2. Check the response status code and body.
3. Send a POST request to /login with a non-existent email.
4. Check the response status code and body.
EXPECTED RESULT: Status code 401 for both steps. Response body indicates invalid credentials.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_AUTH_006
MODULE: Backend API Authentication
DESCRIPTION: Test user login with missing required fields via POST /login.
PRECONDITIONS: Backend server is running.
TEST STEPS:
1. Send a POST request to /login with missing email (only password).
2. Check the response status code and body.
3. Send a POST request to /login with missing password (only email).
4. Check the response status code and body.
5. Send a POST request to /login with empty body.
6. Check the response status code and body.
EXPECTED RESULT: Status code 400 for all steps. Response body indicates missing fields.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_USER_001
MODULE: Backend User Profile API
DESCRIPTION: Test accessing own user profile via GET /users/{user_id}.
PRECONDITIONS: User is logged in and has a valid token. User ID is known.
TEST STEPS:
1. Get the user's ID from the login response.
2. Send a GET request to /users/{user_id} with the Authorization: Bearer {token} header.
3. Check the response status code.
4. Check the response body contains the correct user details (id, email, role).
EXPECTED RESULT: Status code 200. Response body contains the correct user information.
PRIORITY: High
TEST TYPE: API Functional, Security
STATUS: Not Executed

TEST CASE ID: BE_API_USER_002
MODULE: Backend User Profile API
DESCRIPTION: Test accessing another user's profile without admin role via GET /users/{user_id}.
PRECONDITIONS: Two non-admin users exist. User A is logged in. User B's ID is known.
TEST STEPS:
1. Get User A's token and User B's ID.
2. Send a GET request to /users/{User_B_ID} with User A's Authorization: Bearer {token} header.
3. Check the response status code and body.
EXPECTED RESULT: Status code 403. Response body indicates unauthorized.
PRIORITY: High
TEST TYPE: API Functional, Security
STATUS: Not Executed

TEST CASE ID: BE_API_USER_003
MODULE: Backend User Profile API
DESCRIPTION: Test accessing a non-existent user profile via GET /users/{user_id}.
PRECONDITIONS: An admin user is logged in and has a valid token. A non-existent user ID (e.g., 9999) is known.
TEST STEPS:
1. Get the admin user's token.
2. Send a GET request to /users/9999 with the admin's Authorization: Bearer {token} header.
3. Check the response status code and body.
EXPECTED RESULT: Status code 404. Response body indicates user not found.
PRIORITY: Medium
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_ADDRESS_001
MODULE: Backend Address API
DESCRIPTION: Test adding a new shipping address via POST /users/{user_id}/addresses.
PRECONDITIONS: A buyer user is logged in and has a valid token. User ID is known.
TEST STEPS:
1. Get the user's ID and token.
2. Send a POST request to /users/{user_id}/addresses with valid address data (street, city, country).
3. Check the response status code.
4. Check the response body for a success message and address_id.
5. Query the database or use GET /users/{user_id}/addresses to verify the address was added.
EXPECTED RESULT: Status code 201. Response indicates success. Address record exists in DB for the user.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_ADDRESS_002
MODULE: Backend Address API
DESCRIPTION: Test retrieving user's addresses via GET /users/{user_id}/addresses.
PRECONDITIONS: A buyer user is logged in and has addresses associated. User ID and token are known.
TEST STEPS:
1. Get the user's ID and token.
2. Send a GET request to /users/{user_id}/addresses with the Authorization header.
3. Check the response status code.
4. Check the response body is a list of addresses and matches expected count and details.
EXPECTED RESULT: Status code 200. Response is a list containing the user's addresses.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_ADDRESS_003
MODULE: Backend Address API
DESCRIPTION: Test adding address for another user via POST /users/{user_id}/addresses without admin role.
PRECONDITIONS: Two non-admin users exist. User A is logged in. User B's ID is known.
TEST STEPS:
1. Get User A's token and User B's ID.
2. Send a POST request to /users/{User_B_ID}/addresses with User A's Authorization header and valid address data.
3. Check the response status code and body.
EXPECTED RESULT: Status code 403. Response body indicates unauthorized.
PRIORITY: High
TEST TYPE: API Functional, Security
STATUS: Not Executed

TEST CASE ID: BE_API_ADDRESS_004
MODULE: Backend Address API
DESCRIPTION: Test updating a user's address via PUT /addresses/{address_id}.
PRECONDITIONS: A buyer user is logged in and has addresses associated. An address ID belonging to the user is known.
TEST STEPS:
1. Get the user's token and an address ID.
2. Send a PUT request to /addresses/{address_id} with Authorization header and updated address data (e.g., change street).
3. Check the response status code and body.
4. Use GET /users/{user_id}/addresses or query DB to verify the update.
EXPECTED RESULT: Status code 200. Response indicates success. Address is updated in DB.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_ADDRESS_005
MODULE: Backend Address API
DESCRIPTION: Test deleting a user's address via DELETE /addresses/{address_id}.
PRECONDITIONS: A buyer user is logged in and has addresses associated. An address ID belonging to the user is known and is not the only address or the default if others exist.
TEST STEPS:
1. Get the user's token and an address ID.
2. Send a DELETE request to /addresses/{address_id} with Authorization header.
3. Check the response status code and body.
4. Use GET /users/{user_id}/addresses or query DB to verify the address is removed.
EXPECTED RESULT: Status code 200. Response indicates success. Address is removed from DB.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_ADDRESS_006
MODULE: Backend Address API
DESCRIPTION: Test attempting to delete the last remaining address via DELETE /addresses/{address_id}.
PRECONDITIONS: A buyer user is logged in and has only ONE address. The address ID is known.
TEST STEPS:
1. Get the user's token and the single address ID.
2. Send a DELETE request to /addresses/{address_id} with Authorization header.
3. Check the response status code and body.
EXPECTED RESULT: Status code 200 (the code allows deleting the last one). Response indicates success. Address is removed. (Note: Spec didn't forbid this, code allows it).
PRIORITY: Medium
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_ADDRESS_007
MODULE: Backend Address API
DESCRIPTION: Test attempting to delete the default address when other addresses exist via DELETE /addresses/{address_id}.
PRECONDITIONS: A buyer user is logged in and has at least two addresses, one of which is marked default. The default address ID is known.
TEST STEPS:
1. Get the user's token and the default address ID.
2. Send a DELETE request to /addresses/{address_id} with Authorization header.
3. Check the response status code and body.
EXPECTED RESULT: Status code 400. Response body indicates the default address cannot be deleted if others exist (based on backend code logic).
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_PRODUCTS_001
MODULE: Backend Product API (Public)
DESCRIPTION: Test retrieving all approved products via GET /products.
PRECONDITIONS: Backend server is running. Some approved products exist in the DB. Some unapproved products may exist.
TEST STEPS:
1. Send a GET request to /products (no authentication needed).
2. Check the response status code.
3. Check the response body is a list of products.
4. Verify only approved products are in the list.
5. Verify key details are included (id, name, price, stock, image_url, seller_id, seller_shop_name).
EXPECTED RESULT: Status code 200. Response is a list containing only approved products with correct public details.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_PRODUCTS_002
MODULE: Backend Product API (Public)
DESCRIPTION: Test retrieving detail for an approved product via GET /products/{product_id}.
PRECONDITIONS: An approved product with a known ID exists. Some reviews might exist for it.
TEST STEPS:
1. Get the ID of an approved product.
2. Send a GET request to /products/{product_id}.
3. Check the response status code.
4. Check the response body contains full product details (description, seller info, reviews if any).
EXPECTED RESULT: Status code 200. Response contains detailed information for the specific product, including reviews.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_PRODUCTS_003
MODULE: Backend Product API (Public)
DESCRIPTION: Test attempting to retrieve detail for an unapproved product via GET /products/{product_id}.
PRECONDITIONS: An unapproved product with a known ID exists.
TEST STEPS:
1. Get the ID of an unapproved product.
2. Send a GET request to /products/{product_id}.
3. Check the response status code and body.
EXPECTED RESULT: Status code 404. Response body indicates product not found or not approved.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_PRODUCTS_004
MODULE: Backend Product API (Public)
DESCRIPTION: Test attempting to retrieve detail for a non-existent product via GET /products/{product_id}.
PRECONDITIONS: Backend server is running. A non-existent product ID (e.g., 9999) is known.
TEST STEPS:
1. Send a GET request to /products/9999.
2. Check the response status code and body.
EXPECTED RESULT: Status code 404. Response body indicates product not found or not approved.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_PRODUCTS_005
MODULE: Backend Product API (Seller)
DESCRIPTION: Test creating a new product via POST /products (as approved seller).
PRECONDITIONS: An approved seller user is logged in and has a valid token.
TEST STEPS:
1. Get the seller's token.
2. Prepare valid product data (name, description, price, stock, image_url).
3. Send a POST request to /products with Authorization header and product data.
4. Check the response status code and body.
5. Query the DB to verify the product is created, associated with the seller, and has `is_approved=False`.
EXPECTED RESULT: Status code 201. Response indicates success and includes product_id. Product exists in DB, associated with seller, and is unapproved.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_PRODUCTS_006
MODULE: Backend Product API (Seller)
DESCRIPTION: Test creating a new product via POST /products (as buyer).
PRECONDITIONS: A buyer user is logged in and has a valid token.
TEST STEPS:
1. Get the buyer's token.
2. Prepare valid product data.
3. Send a POST request to /products with Authorization header and product data.
4. Check the response status code and body.
EXPECTED RESULT: Status code 403. Response body indicates unauthorized.
PRIORITY: High
TEST TYPE: API Functional, Security
STATUS: Not Executed

TEST CASE ID: BE_API_PRODUCTS_007
MODULE: Backend Product API (Seller)
DESCRIPTION: Test updating an existing product via PUT /products/{product_id} (as its seller).
PRECONDITIONS: An approved seller user is logged in and has a valid token. The seller owns an existing product.
TEST STEPS:
1. Get the seller's token and one of their product IDs.
2. Prepare updated product data (e.g., new price, new stock).
3. Send a PUT request to /products/{product_id} with Authorization header and updated data.
4. Check the response status code and body.
5. Query the DB to verify the product details are updated and `is_approved` is set back to `False`.
EXPECTED RESULT: Status code 200. Response indicates success. Product in DB has updated details and `is_approved=False`.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_PRODUCTS_008
MODULE: Backend Product API (Seller)
DESCRIPTION: Test attempting to update a product owned by another seller via PUT /products/{product_id}.
PRECONDITIONS: Two approved seller users exist (Seller A and Seller B). Seller A is logged in. Seller B owns a product with a known ID.
TEST STEPS:
1. Get Seller A's token and Seller B's product ID.
2. Prepare updated product data.
3. Send a PUT request to /products/{Seller_B_Product_ID} with Seller A's Authorization header and updated data.
4. Check the response status code and body.
EXPECTED RESULT: Status code 403. Response body indicates unauthorized.
PRIORITY: High
TEST TYPE: API Functional, Security
STATUS: Not Executed

TEST CASE ID: BE_API_PRODUCTS_009
MODULE: Backend Product API (Seller)
DESCRIPTION: Test deleting an existing product via DELETE /products/{product_id} (as its seller).
PRECONDITIONS: An approved seller user is logged in and has a valid token. The seller owns an existing product that is NOT in any cart or order.
TEST STEPS:
1. Get the seller's token and one of their product IDs (that is not in carts/orders).
2. Send a DELETE request to /products/{product_id} with Authorization header.
3. Check the response status code and body.
4. Query the DB to verify the product record is deleted.
EXPECTED RESULT: Status code 200. Response indicates success. Product is removed from DB.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_PRODUCTS_010
MODULE: Backend Product API (Seller)
DESCRIPTION: Test attempting to delete a product that IS in a cart or order via DELETE /products/{product_id}.
PRECONDITIONS: An approved seller user is logged in. The seller owns a product with a known ID that exists in at least one active cart or order.
TEST STEPS:
1. Get the seller's token and the product ID.
2. Send a DELETE request to /products/{product_id} with Authorization header.
3. Check the response status code and body.
4. Query the DB to verify the product still exists.
EXPECTED RESULT: Status code 400. Response body indicates the product cannot be deleted due to associated items. Product is not removed from DB.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_CART_001
MODULE: Backend Cart API
DESCRIPTION: Test adding a product to the cart via POST /cart/add.
PRECONDITIONS: A buyer user is logged in and has a valid token. An approved product with sufficient stock exists.
TEST STEPS:
1. Get the user's token and the product ID.
2. Send a POST request to /cart/add with Authorization header and {"product_id": ..., "quantity": 1}.
3. Check the response status code and body.
4. Query the DB to verify a CartItem record is created for the user and product with quantity 1.
EXPECTED RESULT: Status code 200. Response indicates success. CartItem exists in DB.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_CART_002
MODULE: Backend Cart API
DESCRIPTION: Test adding more quantity of an existing product to the cart.
PRECONDITIONS: A buyer user is logged in and has a valid token. The user already has the product in their cart. Sufficient stock is available for the added quantity.
TEST STEPS:
1. Get the user's token and the product ID.
2. Add quantity 1 of the product to the cart (using BE_API_CART_001 steps).
3. Send another POST request to /cart/add with Authorization header and {"product_id": ..., "quantity": 2}.
4. Check the response status code and body.
5. Query the DB to verify the quantity of the CartItem record is updated to 3.
EXPECTED RESULT: Status code 200. Response indicates success. CartItem quantity in DB is updated.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_CART_003
MODULE: Backend Cart API
DESCRIPTION: Test attempting to add more quantity than available stock.
PRECONDITIONS: A buyer user is logged in. A product with low stock (e.g., 5) exists.
TEST STEPS:
1. Get the user's token and the product ID.
2. Send a POST request to /cart/add with Authorization header and {"product_id": ..., "quantity": 6}.
3. Check the response status code and body.
4. Query the DB to verify no CartItem was added or updated for this product.
EXPECTED RESULT: Status code 400. Response body indicates insufficient stock. Cart remains unchanged.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_CART_004
MODULE: Backend Cart API
DESCRIPTION: Test retrieving cart contents via GET /cart.
PRECONDITIONS: A buyer user is logged in and has items in their cart.
TEST STEPS:
1. Get the user's token.
2. Send a GET request to /cart with Authorization header.
3. Check the response status code.
4. Check the response body is a list of cart items.
5. Verify details for each item (product name, price, quantity, image_url).
EXPECTED RESULT: Status code 200. Response is a list containing the user's current cart items with correct details.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_CART_005
MODULE: Backend Cart API
DESCRIPTION: Test updating cart item quantity via PUT /cart/update/{item_id}.
PRECONDITIONS: A buyer user is logged in and has items in their cart. A CartItem ID is known. Sufficient stock for the new quantity.
TEST STEPS:
1. Get the user's token and a CartItem ID.
2. Send a PUT request to /cart/update/{item_id} with Authorization header and {"quantity": 3}.
3. Check the response status code and body.
4. Query the DB or use GET /cart to verify the CartItem quantity is updated.
EXPECTED RESULT: Status code 200. Response indicates success. CartItem quantity in DB is updated.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_CART_006
MODULE: Backend Cart API
DESCRIPTION: Test attempting to update cart item quantity beyond stock via PUT /cart/update/{item_id}.
PRECONDITIONS: A buyer user is logged in. A CartItem exists where the product has low stock (e.g., 5 total stock, 2 already in cart). The CartItem ID is known.
TEST STEPS:
1. Get the user's token and the CartItem ID.
2. Send a PUT request to /cart/update/{item_id} with Authorization header and {"quantity": 6}.
3. Check the response status code and body.
4. Query the DB or use GET /cart to verify the CartItem quantity is UNCHANGED.
EXPECTED RESULT: Status code 400. Response body indicates insufficient stock. CartItem quantity is not updated.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_CART_007
MODULE: Backend Cart API
DESCRIPTION: Test removing a cart item via DELETE /cart/remove/{item_id}.
PRECONDITIONS: A buyer user is logged in and has items in their cart. A CartItem ID is known.
TEST STEPS:
1. Get the user's token and a CartItem ID.
2. Send a DELETE request to /cart/remove/{item_id} with Authorization header.
3. Check the response status code and body.
4. Query the DB or use GET /cart to verify the CartItem record is deleted.
EXPECTED RESULT: Status code 200. Response indicates success. CartItem is removed from DB.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_ORDER_001
MODULE: Backend Order API
DESCRIPTION: Test creating an order from the cart via POST /orders.
PRECONDITIONS: A buyer user is logged in and has a valid token. The user has items in their cart. The user has at least one shipping address. All items in the cart are for approved products with sufficient stock.
TEST STEPS:
1. Get the user's token and a valid shipping address ID.
2. Ensure the user's cart is populated with items meeting preconditions.
3. Note the current stock levels of products in the cart.
4. Send a POST request to /orders with Authorization header and {"shipping_address_id": ...}.
5. Check the response status code and body.
6. Query the DB to verify a new Order record is created with status 'processing' and correct total amount.
7. Query the DB to verify OrderItem records are created linked to the Order.
8. Query the DB to verify all CartItem records for the user are deleted.
9. Query the DB to verify product stock levels are reduced correctly.
EXPECTED RESULT: Status code 201. Response indicates success and includes order_id and status. New Order and OrderItem records exist. Cart is empty. Product stock is reduced.
PRIORITY: High
TEST TYPE: API Functional, Integration, E2E (API level)
STATUS: Not Executed

TEST CASE ID: BE_API_ORDER_002
MODULE: Backend Order API
DESCRIPTION: Test creating an order with an empty cart via POST /orders.
PRECONDITIONS: A buyer user is logged in and has a valid token. The user's cart is empty.
TEST STEPS:
1. Get the user's token.
2. Ensure the user's cart is empty.
3. Send a POST request to /orders with Authorization header and a valid {"shipping_address_id": ...}.
4. Check the response status code and body.
5. Query the DB to verify no new Order was created.
EXPECTED RESULT: Status code 400. Response body indicates cart is empty. No Order record created.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_ORDER_003
MODULE: Backend Order API
DESCRIPTION: Test creating an order with invalid shipping address via POST /orders.
PRECONDITIONS: A buyer user is logged in and has a valid token. The user has items in their cart. An invalid or non-user's shipping address ID is known.
TEST STEPS:
1. Get the user's token.
2. Ensure the user's cart is populated.
3. Send a POST request to /orders with Authorization header and {"shipping_address_id": 9999} (non-existent) OR a valid ID belonging to *another* user.
4. Check the response status code and body.
5. Query the DB to verify no new Order was created.
EXPECTED RESULT: Status code 404 (address not found) or 400 (address does not belong to user - depends on backend error handling, 404 is in code). No Order record created.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_ORDER_004
MODULE: Backend Order API
DESCRIPTION: Test creating an order when a product in the cart is out of stock.
PRECONDITIONS: A buyer user is logged in. The user's cart contains a product that now has 0 stock (stock was reduced after adding to cart) OR contains a quantity greater than current stock.
TEST STEPS:
1. Get the user's token.
2. Manually set the stock of a product in the user's cart to 0 or less than the cart quantity in the DB.
3. Send a POST request to /orders with Authorization header and valid shipping address ID.
4. Check the response status code and body.
5. Query the DB to verify no new Order was created. Query the DB to check if the problematic CartItem was deleted (backend code does this).
EXPECTED RESULT: Status code 400. Response body indicates product unavailable or not enough stock. No Order record created. Problematic CartItem deleted.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_ORDER_005
MODULE: Backend Order API
DESCRIPTION: Test retrieving a buyer's order history via GET /users/{user_id}/orders.
PRECONDITIONS: A buyer user is logged in and has placed orders. User ID and token are known.
TEST STEPS:
1. Get the user's ID and token.
2. Send a GET request to /users/{user_id}/orders with Authorization header.
3. Check the response status code.
4. Check the response body is a list of orders placed by this user.
5. Verify key details for each order (id, total_amount, status, tracking_number, created_at, items list).
6. Verify details for items within orders (product_id, product_name, quantity, price_at_purchase).
EXPECTED RESULT: Status code 200. Response is a list of the buyer's orders with correct details.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_ORDER_006
MODULE: Backend Order API
DESCRIPTION: Test retrieving a specific order detail via GET /orders/{order_id} (as buyer).
PRECONDITIONS: A buyer user is logged in and has placed an order. The order ID belonging to the buyer is known.
TEST STEPS:
1. Get the user's token and one of their order IDs.
2. Send a GET request to /orders/{order_id} with Authorization header.
3. Check the response status code.
4. Check the response body contains detailed information for that specific order.
EXPECTED RESULT: Status code 200. Response contains full order details.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_ORDER_007
MODULE: Backend Order API
DESCRIPTION: Test attempting to retrieve another user's order detail via GET /orders/{order_id} (as buyer).
PRECONDITIONS: Two buyer users exist (User A and User B). User A is logged in. User B has placed an order with a known ID.
TEST STEPS:
1. Get User A's token and User B's order ID.
2. Send a GET request to /orders/{User_B_Order_ID} with User A's Authorization header.
3. Check the response status code and body.
EXPECTED RESULT: Status code 403. Response body indicates unauthorized.
PRIORITY: High
TEST TYPE: API Functional, Security
STATUS: Not Executed

TEST CASE ID: BE_API_ORDER_008
MODULE: Backend Order API (Seller)
DESCRIPTION: Test retrieving orders containing the seller's products via GET /seller/me/orders.
PRECONDITIONS: An approved seller user is logged in. There are orders in the system that include products sold by this seller.
TEST STEPS:
1. Get the seller's token.
2. Send a GET request to /seller/me/orders with Authorization header.
3. Check the response status code.
4. Check the response body is a list of relevant orders.
5. Verify that each order in the list contains a `seller_items_in_order` list that ONLY includes products sold by this seller.
6. Verify key order details are present (id, buyer_user_id, buyer_email, status, tracking_number, created_at).
EXPECTED RESULT: Status code 200. Response is a list of orders containing items sold by the logged-in seller, showing only their items within each order entry.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_ORDER_009
MODULE: Backend Order API (Seller)
DESCRIPTION: Test updating order status via PUT /orders/{order_id}/status (as seller of item in order).
PRECONDITIONS: An approved seller user is logged in. An order exists containing a product sold by this seller. The order status is 'processing' or 'shipped'.
TEST STEPS:
1. Get the seller's token and the ID of a relevant order.
2. Send a PUT request to /orders/{order_id}/status with Authorization header and {"status": "shipped"} (if processing) or {"status": "completed"} (if shipped).
3. Check the response status code and body.
4. Query the DB or use GET /orders/{order_id} (as seller or admin) to verify the status update.
EXPECTED RESULT: Status code 200. Response indicates success and new status. Order status updated in DB.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_ORDER_010
MODULE: Backend Order API (Seller)
DESCRIPTION: Test attempting to update order status via PUT /orders/{order_id}/status (as seller with NO items in order).
PRECONDITIONS: Two approved seller users exist (Seller A and Seller B). Seller A is logged in. Seller B has an order containing only their products.
TEST STEPS:
1. Get Seller A's token and the ID of an order that contains NO products sold by Seller A.
2. Send a PUT request to /orders/{order_id}/status with Seller A's Authorization header and a valid status.
3. Check the response status code and body.
4. Query the DB to verify the status is UNCHANGED.
EXPECTED RESULT: Status code 403. Response body indicates unauthorized. Order status is not updated.
PRIORITY: High
TEST TYPE: API Functional, Security
STATUS: Not Executed

TEST CASE ID: BE_API_ORDER_011
MODULE: Backend Order API (Seller)
DESCRIPTION: Test adding tracking number via PUT /orders/{order_id}/tracking (as seller of item in order).
PRECONDITIONS: An approved seller user is logged in. An order exists containing a product sold by this seller. The order status is 'processing' or 'pending'.
TEST STEPS:
1. Get the seller's token and the ID of a relevant order.
2. Send a PUT request to /orders/{order_id}/tracking with Authorization header and {"tracking_number": "TRK123456"}.
3. Check the response status code and body.
4. Query the DB or use GET /orders/{order_id} (as seller or admin) to verify the tracking number is added and status is updated to 'shipped'.
EXPECTED RESULT: Status code 200. Response indicates success and tracking number. Order tracking number is set and status is 'shipped' in DB.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_REVIEW_001
MODULE: Backend Review API
DESCRIPTION: Test adding a review to a purchased product via POST /products/{product_id}/reviews (as buyer).
PRECONDITIONS: A buyer user is logged in. The user has a valid token. The user has placed and completed an order containing the product they want to review. The product is approved. The user has NOT already reviewed this product.
TEST STEPS:
1. Get the user's token and the ID of a purchased, approved product they haven't reviewed.
2. Send a POST request to /products/{product_id}/reviews with Authorization header and {"rating": 5, "comment": "Great product!"}.
3. Check the response status code and body.
4. Query the DB to verify a new Review record is created linked to the user and product with the correct rating and comment.
EXPECTED RESULT: Status code 201. Response indicates success and includes review_id. Review record exists in DB.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_REVIEW_002
MODULE: Backend Review API
DESCRIPTION: Test attempting to add a review to a product NOT purchased by the user.
PRECONDITIONS: A buyer user is logged in. The user has a valid token. An approved product exists that the user has NOT purchased.
TEST STEPS:
1. Get the user's token and the ID of an unpurchased, approved product.
2. Send a POST request to /products/{product_id}/reviews with Authorization header and {"rating": 4, "comment": "Looks good."}.
3. Check the response status code and body.
4. Query the DB to verify no new Review record was created.
EXPECTED RESULT: Status code 403. Response body indicates unauthorized (can only review purchased products). No Review record created.
PRIORITY: High
TEST TYPE: API Functional, Security
STATUS: Not Executed

TEST CASE ID: BE_API_REVIEW_003
MODULE: Backend Review API
DESCRIPTION: Test attempting to add a review as a seller or admin.
PRECONDITIONS: An approved seller or admin user is logged in. They have a valid token. A product they own or an arbitrary product exists.
TEST STEPS:
1. Get the seller's (or admin's) token and a product ID.
2. Send a POST request to /products/{product_id}/reviews with Authorization header and valid review data.
3. Check the response status code and body.
EXPECTED RESULT: Status code 403. Response body indicates unauthorized (only buyers can review).
PRIORITY: High
TEST TYPE: API Functional, Security
STATUS: Not Executed

TEST CASE ID: BE_API_REVIEW_004
MODULE: Backend Review API
DESCRIPTION: Test attempting to add a second review for the same product by the same user.
PRECONDITIONS: A buyer user is logged in. They have a valid token. The user has successfully reviewed a purchased product already.
TEST STEPS:
1. Get the user's token and the ID of the product they have already reviewed.
2. Send a POST request to /products/{product_id}/reviews with Authorization header and new review data.
3. Check the response status code and body.
4. Query the DB to verify only one Review record exists for this user/product.
EXPECTED RESULT: Status code 409. Response body indicates conflict (already reviewed). No new Review record created.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_REVIEW_005
MODULE: Backend Review API
DESCRIPTION: Test retrieving reviews for a product via GET /products/{product_id}/reviews.
PRECONDITIONS: An approved product exists. Some reviews have been added for this product.
TEST STEPS:
1. Get the ID of the product.
2. Send a GET request to /products/{product_id}/reviews.
3. Check the response status code.
4. Check the response body is a list of reviews for that product.
5. Verify key details for each review (id, rating, comment, user_email, created_at).
EXPECTED RESULT: Status code 200. Response is a list of reviews for the specified product.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_SELLER_001
MODULE: Backend Seller API
DESCRIPTION: Test a buyer applying to become a seller via POST /seller/apply.
PRECONDITIONS: A buyer user is logged in and has a valid token. The user does not have an existing seller profile.
TEST STEPS:
1. Get the buyer user's ID and token.
2. Send a POST request to /seller/apply with Authorization header and valid seller data (shop_name).
3. Check the response status code and body.
4. Query the DB to verify a new SellerProfile record is created linked to the user, with `is_approved=False`. Verify the user's `role` is updated to 'seller'.
EXPECTED RESULT: Status code 201. Response indicates success and includes seller_profile_id. SellerProfile record exists in DB, unapproved. User role is 'seller'.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_SELLER_002
MODULE: Backend Seller API
DESCRIPTION: Test attempting to apply to become a seller if already a seller.
PRECONDITIONS: An approved seller user is logged in and has a valid token and seller profile.
TEST STEPS:
1. Get the seller's token.
2. Send a POST request to /seller/apply with Authorization header and valid seller data.
3. Check the response status code and body.
EXPECTED RESULT: Status code 409. Response body indicates user already has a seller profile.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_SELLER_003
MODULE: Backend Seller API
DESCRIPTION: Test retrieving seller's own profile via GET /seller/me.
PRECONDITIONS: An approved seller user is logged in and has a valid token and seller profile.
TEST STEPS:
1. Get the seller's token.
2. Send a GET request to /seller/me with Authorization header.
3. Check the response status code.
4. Check the response body contains the correct seller profile details.
EXPECTED RESULT: Status code 200. Response contains the seller's profile information.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_SELLER_004
MODULE: Backend Seller API
DESCRIPTION: Test attempting to retrieve seller profile via GET /seller/me as a buyer.
PRECONDITIONS: A buyer user is logged in.
TEST STEPS:
1. Get the buyer's token.
2. Send a GET request to /seller/me with Authorization header.
3. Check the response status code and body.
EXPECTED RESULT: Status code 403. Response body indicates unauthorized.
PRIORITY: High
TEST TYPE: API Functional, Security
STATUS: Not Executed

TEST CASE ID: BE_API_SELLER_005
MODULE: Backend Seller API
DESCRIPTION: Test updating seller's own profile via PUT /seller/me.
PRECONDITIONS: An approved seller user is logged in and has a valid token and seller profile.
TEST STEPS:
1. Get the seller's token.
2. Prepare updated seller profile data (e.g., new shop description).
3. Send a PUT request to /seller/me with Authorization header and updated data.
4. Check the response status code and body.
5. Query the DB or use GET /seller/me to verify the update.
EXPECTED RESULT: Status code 200. Response indicates success. Seller profile in DB is updated.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_SELLER_006
MODULE: Backend Seller API
DESCRIPTION: Test retrieving products of a specific seller via GET /seller/{seller_id}/products.
PRECONDITIONS: An approved seller with a known ID exists and has approved products. Some unapproved products might also exist for this seller.
TEST STEPS:
1. Get the ID of an approved seller.
2. Send a GET request to /seller/{seller_id}/products.
3. Check the response status code.
4. Check the response body is a list of products.
5. Verify only the approved products from that specific seller are included.
EXPECTED RESULT: Status code 200. Response is a list containing only the specified seller's approved products.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_SELLER_007
MODULE: Backend Seller API
DESCRIPTION: Test retrieving products for an unapproved seller via GET /seller/{seller_id}/products.
PRECONDITIONS: An unapproved seller with a known ID exists and has products.
TEST STEPS:
1. Get the ID of an unapproved seller.
2. Send a GET request to /seller/{seller_id}/products.
3. Check the response status code and body.
EXPECTED RESULT: Status code 404. Response body indicates seller not found or not approved.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_SELLER_008
MODULE: Backend Seller API
DESCRIPTION: Test requesting payout via POST /seller/payout/request.
PRECONDITIONS: An approved seller user is logged in.
TEST STEPS:
1. Get the seller's token.
2. Send a POST request to /seller/payout/request with Authorization header (body might be empty or contain request details if added).
3. Check the response status code and body.
EXPECTED RESULT: Status code 200. Response indicates success (simulated payout request).
PRIORITY: Medium
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_ADMIN_001
MODULE: Backend Admin API
DESCRIPTION: Test retrieving list of all users via GET /admin/users.
PRECONDITIONS: An admin user is logged in.
TEST STEPS:
1. Get the admin user's token.
2. Send a GET request to /admin/users with Authorization header.
3. Check the response status code.
4. Check the response body is a list containing all users (buyers, sellers, admins).
5. Verify key user details and seller profile info for sellers are included.
EXPECTED RESULT: Status code 200. Response is a list of all users with relevant details.
PRIORITY: High
TEST TYPE: API Functional, Security
STATUS: Not Executed

TEST CASE ID: BE_API_ADMIN_002
MODULE: Backend Admin API
DESCRIPTION: Test attempting to retrieve list of users as non-admin.
PRECONDITIONS: A buyer or seller user is logged in.
TEST STEPS:
1. Get the non-admin user's token.
2. Send a GET request to /admin/users with Authorization header.
3. Check the response status code and body.
EXPECTED RESULT: Status code 403. Response body indicates unauthorized.
PRIORITY: High
TEST TYPE: API Functional, Security
STATUS: Not Executed

TEST CASE ID: BE_API_ADMIN_003
MODULE: Backend Admin API
DESCRIPTION: Test retrieving list of all sellers via GET /admin/sellers.
PRECONDITIONS: An admin user is logged in.
TEST STEPS:
1. Get the admin user's token.
2. Send a GET request to /admin/sellers with Authorization header.
3. Check the response status code.
4. Check the response body is a list containing all seller profiles (approved and unapproved).
5. Verify key seller profile details are included.
EXPECTED RESULT: Status code 200. Response is a list of all seller profiles.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_ADMIN_004
MODULE: Backend Admin API
DESCRIPTION: Test approving a seller application via PUT /admin/sellers/{seller_id}/approve.
PRECONDITIONS: An admin user is logged in. An unapproved seller application with a known ID exists.
TEST STEPS:
1. Get the admin user's token and the unapproved seller's profile ID.
2. Send a PUT request to /admin/sellers/{seller_id}/approve with Authorization header.
3. Check the response status code and body.
4. Query the DB to verify the SellerProfile record has `is_approved=True` and the linked User record has `role='seller'`.
EXPECTED RESULT: Status code 200. Response indicates seller approved. SellerProfile is approved and user role is seller in DB.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_ADMIN_005
MODULE: Backend Admin API
DESCRIPTION: Test retrieving list of all products (approved and unapproved) via GET /admin/products.
PRECONDITIONS: An admin user is logged in. Products (approved and unapproved) exist.
TEST STEPS:
1. Get the admin user's token.
2. Send a GET request to /admin/products with Authorization header.
3. Check the response status code.
4. Check the response body is a list containing all products.
5. Verify `is_approved` status is included for each product.
EXPECTED RESULT: Status code 200. Response is a list of all products, showing their approval status.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_ADMIN_006
MODULE: Backend Admin API
DESCRIPTION: Test approving a product listing via PUT /admin/products/{product_id}/approve.
PRECONDITIONS: An admin user is logged in. An unapproved product listing with a known ID exists.
TEST STEPS:
1. Get the admin user's token and the unapproved product ID.
2. Send a PUT request to /admin/products/{product_id}/approve with Authorization header.
3. Check the response status code and body.
4. Query the DB or use GET /admin/products or public GET /products/{product_id} to verify `is_approved=True`.
EXPECTED RESULT: Status code 200. Response indicates product approved. Product `is_approved` is True in DB.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: BE_API_ADMIN_007
MODULE: Backend Admin API
DESCRIPTION: Test retrieving list of all orders via GET /admin/orders.
PRECONDITIONS: An admin user is logged in. Orders exist in the system.
TEST STEPS:
1. Get the admin user's token.
2. Send a GET request to /admin/orders with Authorization header.
3. Check the response status code.
4. Check the response body is a list containing all orders.
5. Verify key order details are included.
EXPECTED RESULT: Status code 200. Response is a list of all orders in the system.
PRIORITY: High
TEST TYPE: API Functional
STATUS: Not Executed

TEST CASE ID: BE_API_ADMIN_008
MODULE: Backend Admin API
DESCRIPTION: Test generating sales report via GET /admin/reports/sales.
PRECONDITIONS: An admin user is logged in. Some orders with status 'completed' exist.
TEST STEPS:
1. Get the admin user's token.
2. Calculate the expected total revenue from 'completed' orders in the DB.
3. Send a GET request to /admin/reports/sales with Authorization header.
4. Check the response status code.
5. Check the response body contains the total completed sales revenue.
6. Verify the reported revenue matches the expected calculation.
EXPECTED RESULT: Status code 200. Response contains the total completed sales revenue, matching the sum of completed order amounts.
PRIORITY: High
TEST TYPE: API Functional, Integration
STATUS: Not Executed

TEST CASE ID: FE_INT_NAV_001
MODULE: Frontend Navigation
DESCRIPTION: Verify clicking navigation links switches visible view.
PRECONDITIONS: Frontend HTML is loaded in a browser.
TEST STEPS:
1. Observe the initial visible view (should be homepage).
2. Click the "Shop" link in the header navigation.
3. Observe the visible view.
4. Click the "Cart" link/icon.
5. Observe the visible view.
6. Click the "Login" link.
7. Observe the visible view.
8. Click the "Register" link.
9. Observe the visible view.
10. Click the "Home" link.
11. Observe the visible view.
EXPECTED RESULT: Clicking each navigation link makes the corresponding div with the `view` class and `id` matching the `data-view` attribute visible, and hides others.
PRIORITY: High
TEST TYPE: Integration (JS-DOM)
STATUS: Not Executed

TEST CASE ID: FE_INT_HOMEPAGE_001
MODULE: Frontend Homepage
DESCRIPTION: Verify featured products are rendered on the homepage.
PRECONDITIONS: Frontend HTML is loaded. JS `products` array is populated.
TEST STEPS:
1. Load the homepage.
2. Locate the "Featured Products" section.
3. Observe the number of product items displayed in the grid.
4. Verify each item displays an image, name, and price based on the `products` data (specifically the first few items).
EXPECTED RESULT: The first 4 products from the JS `products` array are displayed correctly in the featured section grid.
PRIORITY: High
TEST TYPE: Integration (JS-DOM)
STATUS: Not Executed

TEST CASE ID: FE_INT_PRODUCT_LIST_001
MODULE: Frontend Product List Page
DESCRIPTION: Verify all products are rendered on the Shop page.
PRECONDITIONS: Frontend HTML is loaded. JS `products` array is populated.
TEST STEPS:
1. Click the "Shop" navigation link.
2. Observe the "All Products" section.
3. Observe the number of product items displayed in the grid.
4. Verify all products from the JS `products` array are displayed.
EXPECTED RESULT: All products from the JS `products` array are displayed correctly in the "All Products" grid.
PRIORITY: High
TEST TYPE: Integration (JS-DOM)
STATUS: Not Executed

TEST CASE ID: FE_INT_PRODUCT_DETAIL_001
MODULE: Frontend Product Detail Page
DESCRIPTION: Verify clicking a product item navigates to the detail page and displays correct info.
PRECONDITIONS: Frontend HTML is loaded. Products are displayed on homepage or shop page.
TEST STEPS:
1. Click on any product item displayed on the homepage or shop page.
2. Observe the visible view.
3. Verify the product detail view is displayed.
4. Check if the displayed title, price, description, and image match the clicked product's data from the JS `products` array.
EXPECTED RESULT: The product detail view is shown, displaying accurate details for the selected product.
PRIORITY: High
TEST TYPE: Integration (JS-DOM)
STATUS: Not Executed

TEST CASE ID: FE_INT_CART_001
MODULE: Frontend Cart Functionality
DESCRIPTION: Verify clicking "Add to Cart" on product detail page adds item to cart (JS array) and updates count.
PRECONDITIONS: Frontend HTML is loaded. Product detail page is visible. Cart count is initially 0.
TEST STEPS:
1. Navigate to a product detail page.
2. Click the "Add to Cart" button.
3. Observe the cart count in the header.
4. Check the browser's developer console (if applicable) or the JS `cart` array to confirm the item was added.
5. Click "Add to Cart" again for the same product.
6. Observe the cart count.
7. Check the JS `cart` array quantity for the item.
EXPECTED RESULT: An alert "Product Name added to cart!" appears. The cart count in the header increments (e.g., from 0 to 1, then 1 to 2). The item is added to the JS `cart` array, and quantity updates correctly on subsequent clicks.
PRIORITY: High
TEST TYPE: Integration (JS-DOM, JS Logic)
STATUS: Not Executed

TEST CASE ID: FE_INT_CART_002
MODULE: Frontend Cart Page
DESCRIPTION: Verify cart page displays added items and total.
PRECONDITIONS: Frontend HTML is loaded. Items have been added to the cart (using FE_INT_CART_001).
TEST STEPS:
1. Click the "Cart" icon/link in the header.
2. Observe the "Your Shopping Cart" view.
3. Verify that the added product(s) are listed.
4. Check that each listed item shows the product image, name, price, and quantity input.
5. Check that the "Subtotal" reflects the sum of (price * quantity) for all items in the JS `cart` array.
EXPECTED RESULT: The cart page shows a list of products in the cart. Each item is displayed correctly with its details and current quantity. The subtotal displayed is accurate based on the cart contents.
PRIORITY: High
TEST TYPE: Integration (JS-DOM, JS Logic)
STATUS: Not Executed

TEST CASE ID: FE_INT_CART_003
MODULE: Frontend Cart Functionality
DESCRIPTION: Verify updating quantity on the cart page updates total and JS array.
PRECONDITIONS: Frontend HTML is loaded. Items are displayed on the cart page.
TEST STEPS:
1. On the cart page, change the quantity of an item using the input field (e.g., from 1 to 3).
2. Observe the subtotal.
3. Check the JS `cart` array quantity for the updated item.
EXPECTED RESULT: The subtotal updates immediately to reflect the new quantity. The quantity in the JS `cart` array is updated.
PRIORITY: High
TEST TYPE: Integration (JS-DOM, JS Logic)
STATUS: Not Executed

TEST CASE ID: FE_INT_CART_004
MODULE: Frontend Cart Functionality
DESCRIPTION: Verify removing an item from the cart page updates list, total, and JS array.
PRECONDITIONS: Frontend HTML is loaded. Multiple items are in the cart and displayed on the cart page.
TEST STEPS:
1. On the cart page, click the "Remove" button next to an item.
2. Observe the list of items in the cart.
3. Observe the subtotal.
4. Check the JS `cart` array.
EXPECTED RESULT: The item is removed from the displayed list. The subtotal updates to exclude the removed item's cost. The item is removed from the JS `cart` array.
PRIORITY: High
TEST TYPE: Integration (JS-DOM, JS Logic)
STATUS: Not Executed

TEST CASE ID: FE_INT_CART_005
MODULE: Frontend Cart Functionality
DESCRIPTION: Verify removing the last item results in an empty cart message.
PRECONDITIONS: Frontend HTML is loaded. Only one item is in the cart.
TEST STEPS:
1. On the cart page, click the "Remove" button next to the single item.
2. Observe the list area in the cart view.
3. Observe the subtotal.
4. Check the JS `cart` array.
EXPECTED RESULT: The item is removed. A message like "Your cart is empty." is displayed. The subtotal becomes $0.00. The JS `cart` array is empty.
PRIORITY: High
TEST TYPE: Integration (JS-DOM, JS Logic)
STATUS: Not Executed

TEST CASE ID: FE_INT_CHECKOUT_001
MODULE: Frontend Checkout (Placeholder)
DESCRIPTION: Verify clicking "Proceed to Checkout" navigates to the checkout placeholder page.
PRECONDITIONS: Frontend HTML is loaded. Items are in the cart.
TEST STEPS:
1. On the cart page, click the "Proceed to Checkout" button.
2. Observe the visible view.
EXPECTED RESULT: The checkout placeholder view is displayed.
PRIORITY: Medium
TEST TYPE: Integration (JS-DOM)
STATUS: Not Executed

TEST CASE ID: FE_INT_SEARCH_001
MODULE: Frontend Search (Basic JS)
DESCRIPTION: Verify search input and button are present. (Note: Frontend search is not implemented to filter `products` array or call backend).
PRECONDITIONS: Frontend HTML is loaded.
TEST STEPS:
1. Observe the header area.
2. Verify a text input field and a button labeled "Search" are present within the search bar div.
3. (Conceptual only for provided code): Enter text and click the button. Observe no filtering happens in the provided JS.
EXPECTED RESULT: Search input and button are visible in the header. (Frontend functionality beyond appearance is not expected from provided JS).
PRIORITY: Low
TEST TYPE: Integration (DOM structure)
STATUS: Not Executed

TEST CASE ID: E2E_BUY_001
MODULE: End-to-End Buyer Flow (API Level Simulation)
DESCRIPTION: Simulate a full buyer journey from registration to order placement using API calls.
PRECONDITIONS: Backend server is running. Initial data is set up (approved products, admin user exists).
TEST STEPS:
1. Use API POST /register to create a new buyer user.
2. Use API POST /login with the new user's credentials to get a token.
3. Use API POST /users/{user_id}/addresses to add a shipping address for the user.
4. Use API GET /products to find an approved product ID.
5. Use API POST /cart/add to add the product to the user's cart.
6. Use API GET /cart to verify the item is in the cart.
7. Use API POST /orders to create an order from the cart, referencing the shipping address ID.
8. Check the response status code and body from /orders call.
9. Use API GET /users/{user_id}/orders to verify the new order appears in the user's order history.
10. Use API GET /orders/{order_id} to retrieve details of the specific order.
EXPECTED RESULT: All API calls are successful (201, 200 status codes where expected). User, address, cart item, and order records are created in the DB. Cart is cleared after order. Order history shows the new order.
PRIORITY: High
TEST TYPE: End-to-End (API)
STATUS: Not Executed

TEST CASE ID: E2E_SELLER_001
MODULE: End-to-End Seller Flow (API Level Simulation)
DESCRIPTION: Simulate seller application and product listing process using API calls.
PRECONDITIONS: Backend server is running. Initial data is set up (admin user exists).
TEST STEPS:
1. Use API POST /register to create a new user with role 'buyer'.
2. Use API POST /login with the new user's credentials to get a token.
3. Use API POST /seller/apply to submit a seller application for this user.
4. Check response indicates awaiting admin approval.
5. Use API POST /login with admin credentials to get admin token.
6. Use API GET /admin/sellers to find the new unapproved seller application ID.
7. Use API PUT /admin/sellers/{seller_id}/approve with admin token to approve the seller.
8. Check response indicates seller approved.
9. Use API POST /login with the seller's credentials again (or verify role update if token valid).
10. Use API GET /seller/me to verify the seller profile is approved.
11. Use API POST /products as the seller to create a new product.
12. Check response indicates product awaiting admin approval.
13. Use API GET /admin/products to find the new unapproved product ID.
14. Use API PUT /admin/products/{product_id}/approve with admin token to approve the product.
15. Check response indicates product approved.
16. Use API GET /products (public endpoint) or /products/{product_id} to verify the product is now publicly visible and approved.
EXPECTED RESULT: All API calls are successful (201, 200 status codes where expected). Seller profile created and approved. User role becomes seller. Product created and approved, becoming publicly visible.
PRIORITY: High
TEST TYPE: End-to-End (API)
STATUS: Not Executed

TEST CASE ID: E2E_ADMIN_001
MODULE: End-to-End Admin Flow (API Level Simulation)
DESCRIPTION: Simulate core admin tasks: user/seller/product/order monitoring and approval using API calls.
PRECONDITIONS: Backend server is running. Various users (buyers, sellers - approved/pending), products (approved/unapproved), and orders exist. Admin user credentials are known.
TEST STEPS:
1. Use API POST /login with admin credentials to get admin token.
2. Use API GET /admin/users to list and verify users.
3. Use API GET /admin/sellers to list and verify seller applications.
4. Use API PUT /admin/sellers/{unapproved_seller_id}/approve to approve a seller.
5. Use API GET /admin/products to list and verify products by approval status.
6. Use API PUT /admin/products/{unapproved_product_id}/approve to approve a product.
7. Use API GET /admin/orders to list and verify all orders.
8. Use API GET /orders/{order_id} with admin token to view details of an order.
9. Use API PUT /orders/{order_id}/status with admin token to update order status.
10. Use API GET /admin/reports/sales to retrieve sales report.
EXPECTED RESULT: All API calls are successful (200 status codes). Admin can retrieve comprehensive lists, approve entities, view order details, update statuses, and get reports.
PRIORITY: High
TEST TYPE: End-to-End (API)
STATUS: Not Executed

TEST CASE ID: SEC_AUTH_001
MODULE: Security - Authentication
DESCRIPTION: Verify API endpoints requiring authentication return 401 or 403 without token.
PRECONDITIONS: Backend server is running. API endpoints like /cart, /orders, /seller/me, /admin/users etc. exist.
TEST STEPS:
1. Choose an endpoint that requires authentication (e.g., GET /cart).
2. Send a GET request to the endpoint *without* an Authorization header.
3. Check the response status code.
4. Send a GET request to the endpoint with an invalid or expired Authorization header (e.g., Bearer invalid_token).
5. Check the response status code.
EXPECTED RESULT: Status code 401 or 403 depending on endpoint design (code uses 401 for missing/invalid token, 403 for unauthorized role). Response body indicates authentication/authorization failure.
PRIORITY: High
TEST TYPE: Security, API Functional
STATUS: Not Executed

TEST CASE ID: SEC_INJECTION_001
MODULE: Security - Injection (Conceptual)
DESCRIPTION: Test basic SQL Injection attempts on API inputs. (Note: SQLAlchemy provides protection, this is a verification check).
PRECONDITIONS: Backend server is running. Endpoints accepting string inputs (e.g., search, registration, update endpoints) are available.
TEST STEPS:
1. Choose an API endpoint that takes string input (e.g., product description in PUT /products/{product_id}).
2. Send a request with crafted input like `' OR '1'='1` or `; DROP TABLE users; --`.
3. Observe the response and backend logs/database state.
4. Choose an endpoint that takes numeric input (e.g., price in POST /products).
5. Send a request with non-numeric or crafted input like `10; DROP TABLE products;`.
6. Observe the response and backend logs/database state.
EXPECTED RESULT: The application handles the input safely. Database structure and data are unaffected. The API returns appropriate error responses (e.g., 400 Bad Request) or processes the input as literal string data where applicable (e.g., in descriptions).
PRIORITY: High
TEST TYPE: Security
STATUS: Not Executed

TEST CASE ID: PERF_LOAD_001
MODULE: Performance
DESCRIPTION: Test basic page load times for key public pages. (Manual or simple tooling).
PRECONDITIONS: Frontend is deployed. Backend is running.
TEST STEPS:
1. Using browser developer tools or a simple online tool, measure the load time for the homepage (/index.html).
2. Measure the load time for the Shop page (/index.html navigated to shop view).
3. Measure the load time for a product detail page (/index.html navigated to detail view).
EXPECTED RESULT: Pages load within a reasonable time frame (e.g., under 3 seconds, though highly dependent on environment and content).
PRIORITY: Medium
TEST TYPE: Performance
STATUS: Not Executed

TEST CASE ID: USABILITY_NAV_001
MODULE: Usability - Navigation
DESCRIPTION: Evaluate ease of navigating between main sections using header links and cart icon.
PRECONDITIONS: Frontend is deployed.
TEST STEPS:
1. As a new user, try to find the shop page.
2. As a user browsing products, try to locate the cart.
3. From any page, try to return to the homepage.
EXPECTED RESULT: Navigation links are clearly labeled and easily accessible. Clicking links predictably changes the view.
PRIORITY: Medium
TEST TYPE: Usability
STATUS: Not Executed

TEST CASE ID: USABILITY_CART_001
MODULE: Usability - Cart Management
DESCRIPTION: Evaluate ease of adding, updating, and removing items from the cart.
PRECONDITIONS: Frontend is deployed. Products are available for adding to cart.
TEST STEPS:
1. Find a product and add it to the cart. Observe feedback (alert, count update).
2. Go to the cart page. Change the quantity of the item. Observe feedback (subtotal update).
3. Remove the item from the cart. Observe feedback (item removed, subtotal update, empty cart message).
EXPECTED RESULT: Actions like adding, updating quantity, and removing items are intuitive. Visual feedback is clear and immediate.
PRIORITY: Medium
TEST TYPE: Usability
STATUS: Not Executed

--- End of Test Cases ---