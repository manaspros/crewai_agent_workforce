# This is the start of the single Python deliverable file.
# Backend Engineer 1's code would go here (DB setup, User models, Auth routes, Admin User routes)
# Backend Engineer 2's code would go here (Product models, Category/Tag models, Product routes, Search, Admin Product routes)
# Backend Engineer 3's code goes below.

import uuid
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from datetime import datetime # Used for simulated timestamps

# --- Conceptual Flask App Setup ---
# This is a simplified representation. A real app would have proper config and structure.
# Engineer 1 would typically handle the main Flask app initialization and configuration.
# The following lines would likely be part of Engineer 1's initial setup code.
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-engineer1-base-key-replace-me" # Main secret
jwt = JWTManager(app)

# --- Simulated Database ---
# In a real application, this would be a database (SQLAlchemy, Django ORM, etc.)
# Data structures simulating tables using in-memory dictionaries.
# Engineer 1 would define and manage the actual database models and connection.
# These dictionaries are shared conceptual data structures.
# For Engineer 3's code to work in isolation for testing, they need minimal versions of shared data.
# In the final merged file, these would be the actual database interfaces.
users_db = {
    "user1_cust": {"id": "user1_cust", "email": "customer1@example.com", "password_hash": "hashed_password", "role": "customer", "is_approved_seller": False, "profile": {"name": "Customer User", "shipping_address": "123 Customer St, Anytown, CA 91234"}},
    "user2_seller": {"id": "user2_seller", "email": "seller1@example.com", "password_hash": "hashed_password", "role": "seller", "is_approved_seller": True, "profile": {"shop_name": "Seller Shop A", "bio": "We make stuff A"}},
    "user3_admin": {"id": "user3_admin", "email": "admin1@example.com", "password_hash": "hashed_password", "role": "admin", "is_approved_seller": True, "profile": {}},
    "user4_seller": {"id": "user4_seller", "email": "seller2@example.com", "password_hash": "hashed_password", "role": "seller", "is_approved_seller": True, "profile": {"shop_name": "Crafty Goods B", "bio": "Unique crafts B"}},
    "user5_cust": {"id": "user5_cust", "email": "customer2@example.com", "password_hash": "hashed_password", "role": "customer", "is_approved_seller": False, "profile": {"name": "Another Customer", "shipping_address": "456 Another Ave, Sometown, NY 56789"}},
}

products_db = {
    "prod1_mug": {"id": "prod1_mug", "title": "Ceramic Mug", "description": "Handmade mug", "price": 25.00, "quantity": 15, "seller_id": "user2_seller", "category_id": "cat1_pottery", "image_urls": ["/images/prod1_mug_1.jpg", "/images/prod1_mug_2.jpg"], "status": "active"},
    "prod2_scarf": {"id": "prod2_scarf", "title": "Knitted Scarf", "description": "Soft wool scarf", "price": 35.00, "quantity": 8, "seller_id": "user2_seller", "category_id": "cat2_textiles", "image_urls": ["/images/prod2_scarf_1.jpg"], "status": "active"},
    "prod3_birdhouse": {"id": "prod3_birdhouse", "title": "Wooden Birdhouse", "description": "Hand-carved birdhouse", "price": 55.00, "quantity": 5, "seller_id": "user4_seller", "category_id": "cat3_wood", "image_urls": ["/images/prod3_birdhouse_1.jpg"], "status": "active"},
    "prod4_earrings": {"id": "prod4_earrings", "title": "Silver Earrings", "description": "Delicate silver earrings", "price": 40.00, "quantity": 20, "seller_id": "user4_seller", "category_id": "cat4_jewelry", "image_urls": ["/images/prod4_earrings_1.jpg", "/images/prod4_earrings_2.jpg"], "status": "active"},
     "prod5_inactive": {"id": "prod5_inactive", "title": "Inactive Item", "description": "Not available", "price": 10.00, "quantity": 0, "seller_id": "user2_seller", "category_id": "cat99_other", "image_urls": [], "status": "inactive"},
}

# Cart simulation: map user_id to a list of cart items {product_id: str, quantity: int}
carts_db = {
    "user1_cust": [{"product_id": "prod1_mug", "quantity": 1}, {"product_id": "prod2_scarf", "quantity": 2}]
}

# Order simulation: map order_id to order details
# Example order data, simulating orders already created
orders_db = {
    "order_abc": {
        "id": "order_abc",
        "user_id": "user1_cust",
        "order_date": "2023-10-25T10:00:00Z",
        "total_amount": 105.00, # 25.00*1 + 35.00*2
        "shipping_address": "123 Customer St, Anytown, CA 91234",
        "status": "processing", # Example status
        "payment_status": "paid",
        "tracking_number": None,
        "items": [
            {"product_id": "prod1_mug", "quantity": 1, "price_at_purchase": 25.00, "seller_id": "user2_seller"},
            {"product_id": "prod2_scarf", "quantity": 2, "price_at_purchase": 35.00, "seller_id": "user2_seller"}
        ]
    },
     "order_def": {
        "id": "order_def",
        "user_id": "user5_cust",
        "order_date": "2023-10-26T14:30:00Z",
        "total_amount": 55.00,
        "shipping_address": "456 Another Ave, Sometown, NY 56789",
        "status": "shipped",
        "payment_status": "paid",
        "tracking_number": "TRACKXYZ789",
        "items": [
            {"product_id": "prod3_birdhouse", "quantity": 1, "price_at_purchase": 55.00, "seller_id": "user4_seller"}
        ]
    },
     "order_ghi": { # Order with multiple sellers
        "id": "order_ghi",
        "user_id": "user1_cust",
        "order_date": "2023-10-26T16:00:00Z",
        "total_amount": 65.00, # 25 + 40
        "shipping_address": "123 Customer St, Anytown, CA 91234",
        "status": "processing",
        "payment_status": "paid",
        "tracking_number": None,
        "items": [
            {"product_id": "prod1_mug", "quantity": 1, "price_at_purchase": 25.00, "seller_id": "user2_seller"},
            {"product_id": "prod4_earrings", "quantity": 1, "price_at_purchase": 40.00, "seller_id": "user4_seller"}
        ]
    },
     "order_jkl": { # Pending payment order
         "id": "order_jkl",
         "user_id": "user5_cust",
         "order_date": "2023-10-27T09:00:00Z",
         "total_amount": 80.00, # 2 x prod4
         "shipping_address": "456 Another Ave, Sometown, NY 56789",
         "status": "pending_payment",
         "payment_status": "pending",
         "tracking_number": None,
         "items": [
            {"product_id": "prod4_earrings", "quantity": 2, "price_at_purchase": 40.00, "seller_id": "user4_seller"}
         ]
     }
}

reviews_db = {
    "review1": {"id": "review1", "product_id": "prod1_mug", "user_id": "user1_cust", "rating": 5, "comment": "Love this mug, great quality!", "review_date": "2023-10-26T11:00:00Z"},
     "review2": {"id": "review2", "product_id": "prod3_birdhouse", "user_id": "user5_cust", "rating": 4, "comment": "Beautiful craftsmanship.", "review_date": "2023-10-27T15:00:00Z"},
}

# --- Helper Functions (Simulated Authentication & Roles) ---
# Engineer 1 would implement robust versions of these using actual password hashing and database queries.
# These helper functions would be defined by Engineer 1.
def get_user_from_identity(identity):
    """Retrieve user object from JWT identity."""
    # In a real app, query the database: User.query.get(identity)
    return users_db.get(identity)

def customer_required(fn):
    """Decorator to check if user is a customer."""
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = get_user_from_identity(current_user_id)
        if not user or user.get('role') != 'customer':
            return jsonify({"msg": "Customers only!"}), 403
        return fn(*args, **kwargs)
    # Fix for Flask-JWT-Extended decorators on Flask 2.3+ if needed depending on Flask version
    wrapper.__name__ = fn.__name__
    return wrapper

def seller_required(fn):
    """Decorator to check if user is a seller."""
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = get_user_from_identity(current_user_id)
        # Also check if the seller is approved if that flow exists
        if not user or user.get('role') != 'seller' or not user.get('is_approved_seller', False):
            return jsonify({"msg": "Sellers only or seller not approved!"}), 403
        return fn(*args, **kwargs)
    # Fix for Flask-JWT-Extended decorators on Flask 2.3+ if needed
    wrapper.__name__ = fn.__name__
    return wrapper

def admin_required(fn):
    """Decorator to check if user is an admin."""
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = get_user_from_identity(current_user_id)
        if not user or user.get('role') != 'admin':
            return jsonify({"msg": "Admins only!"}), 403
        return fn(*args, **kwargs)
    # Fix for Flask-JWT-Extended decorators on Flask 2.3+ if needed
    wrapper.__name__ = fn.__name__
    return wrapper

# --- Helper Function for Email Notifications ---
# Simulated email sending function (Engineer 3)
def send_email_notification(recipient_email, subject, body):
    """
    Simulates sending an email.
    In a real app, this would integrate with SendGrid, Mailgun, etc.
    Engineer 3 would be responsible for this utility.
    This helper function could be placed here or in a shared utilities section.
    """
    print(f"\n--- Simulating Email Notification ---")
    print(f"To: {recipient_email}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")
    print(f"-------------------------------------\n")
    # Real implementation would call an email service API


# --- Backend Engineer 3 Assigned Endpoints & Logic ---

# Shopping Cart Endpoints (Engineer 3)
@app.route('/api/cart', methods=['GET'])
@jwt_required() # Assuming cart is tied to logged-in user for this demo
def get_cart():
    user_id = get_jwt_identity()
    cart_items = carts_db.get(user_id, [])

    detailed_cart = []
    for item in cart_items:
        # Need to access products_db, which is a shared resource
        product = products_db.get(item['product_id'])
        if product and product.get('status') == 'active': # Only include active products
            detailed_cart.append({
                "product_id": product['id'],
                "title": product['title'],
                "price": product['price'],
                "quantity": item['quantity'],
                "image_url": product['image_urls'][0] if product['image_urls'] else None # Use first image
            })
        # Optionally, handle cases where product is inactive/deleted - maybe remove from cart?
    return jsonify(detailed_cart), 200

@app.route('/api/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id or not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"msg": "Invalid product ID or quantity"}), 400

    # Need to access products_db
    product = products_db.get(product_id)
    if not product or product.get('status') != 'active':
        return jsonify({"msg": "Product not found or not available"}), 404

    # Check stock *before* attempting to add/update
    current_cart_quantity = next((item['quantity'] for item in carts_db.get(user_id, []) if item['product_id'] == product_id), 0)
    if product['quantity'] < current_cart_quantity + quantity:
        return jsonify({"msg": f"Insufficient stock. Adding {quantity} to current {current_cart_quantity} would exceed available {product['quantity']}."}), 400

    # Initialize cart if it doesn't exist for the user
    if user_id not in carts_db:
        carts_db[user_id] = []

    # Check if product is already in cart
    cart_item_exists = False
    for item in carts_db[user_id]:
        if item['product_id'] == product_id:
            # Update quantity
            item['quantity'] += quantity
            cart_item_exists = True
            break

    if not cart_item_exists:
        # Add new item to cart
        carts_db[user_id].append({"product_id": product_id, "quantity": quantity})

    return jsonify({"msg": "Product added to cart"}), 200

@app.route('/api/cart/<product_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(product_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    new_quantity = data.get('quantity')

    if not isinstance(new_quantity, int) or new_quantity < 0:
        return jsonify({"msg": "Invalid quantity"}), 400

    cart_items = carts_db.get(user_id, [])
    item_found = False
    for item in cart_items:
        if item['product_id'] == product_id:
            item_found = True
            if new_quantity == 0:
                # Remove item if quantity is 0
                carts_db[user_id].remove(item)
                if not carts_db[user_id]:
                    del carts_db[user_id] # Remove user entry if cart is empty
                return jsonify({"msg": "Product removed from cart"}), 200
            else:
                # Check stock for new quantity
                # Need to access products_db
                product = products_db.get(product_id)
                if not product or product.get('status') != 'active':
                     return jsonify({"msg": "Product not found or not available"}), 404 # Product might have become inactive
                if product['quantity'] < new_quantity:
                    return jsonify({"msg": f"Insufficient stock. Only {product['quantity']} available for '{product['title']}'"}), 400

                item['quantity'] = new_quantity
                return jsonify({"msg": "Cart updated"}), 200

    if not item_found:
         return jsonify({"msg": "Product not found in cart"}), 404

@app.route('/api/cart/<product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(product_id):
    user_id = get_jwt_identity()
    cart_items = carts_db.get(user_id, [])
    item_to_remove = None
    for item in cart_items:
        if item['product_id'] == product_id:
            item_to_remove = item
            break

    if item_to_remove:
        carts_db[user_id].remove(item_to_remove)
        if not carts_db[user_id]:
            del carts_db[user_id] # Remove user entry if cart is empty
        return jsonify({"msg": "Product removed from cart"}), 200
    else:
        return jsonify({"msg": "Product not found in cart"}), 404


# Order Creation & Payment Endpoints (Engineer 3)

@app.route('/api/checkout/create-order', methods=['POST'])
@customer_required
def create_order():
    user_id = get_jwt_identity()
    user = users_db.get(user_id) # Need to access users_db

    data = request.get_json()
    shipping_address = data.get('shipping_address')

    if not shipping_address:
        # Attempt to use profile address if available
        shipping_address = user['profile'].get('shipping_address')
        if not shipping_address:
            return jsonify({"msg": "Shipping address is required"}), 400

    cart_items = carts_db.get(user_id, [])
    if not cart_items:
        return jsonify({"msg": "Cart is empty"}), 400

    order_items_list = []
    total_amount = 0
    inventory_updates = {} # To track changes before committing

    # Validate cart items, calculate total, and prepare inventory updates
    # --- Simulate Transaction Start --- (Conceptual in memory)
    try:
        for item in cart_items:
            product_id = item['product_id']
            quantity = item['quantity']
            product = products_db.get(product_id) # Need to access products_db

            if not product or product.get('status') != 'active':
                return jsonify({"msg": f"Product '{product.get('title', product_id)}' is no longer available."}), 400
            if product['quantity'] < quantity:
                return jsonify({"msg": f"Insufficient stock for '{product['title']}'. Only {product['quantity']} available."}), 400

            item_price = product['price']
            order_items_list.append({
                "product_id": product_id,
                "quantity": quantity,
                "price_at_purchase": item_price,
                "seller_id": product['seller_id'] # Store seller_id with item for easy lookup later (Access products_db)
            })
            total_amount += item_price * quantity
            inventory_updates[product_id] = product['quantity'] - quantity

        if not order_items_list:
             return jsonify({"msg": "No valid items in cart"}), 400

        # Apply inventory updates (Conceptual)
        for product_id, new_quantity in inventory_updates.items():
            products_db[product_id]['quantity'] = new_quantity # Update products_db

        # Create the order
        order_id = str(uuid.uuid4()) # Generate unique ID
        new_order = {
            "id": order_id,
            "user_id": user_id,
            "order_date": datetime.utcnow().isoformat() + 'Z', # Use actual timestamp
            "total_amount": total_amount,
            "shipping_address": shipping_address,
            "status": "pending_payment", # Set status indicating waiting for payment
            "payment_status": "pending",
            "tracking_number": None,
            "items": order_items_list
        }
        orders_db[order_id] = new_order # Update orders_db

        # Clear the user's cart after order creation
        if user_id in carts_db:
             del carts_db[user_id] # Update carts_db

        # --- Simulate Transaction Commit ---
        return jsonify({"msg": "Order created successfully, proceed to payment", "order_id": order_id, "total_amount": total_amount}), 201

    except Exception as e:
        # --- Simulate Transaction Rollback ---
        # In a real DB, rollback changes.
        print(f"Error during order creation: {e}. Simulating rollback.")
        return jsonify({"msg": "Failed to create order", "error": str(e)}), 500


@app.route('/api/checkout/initiate-payment', methods=['POST'])
@customer_required
def initiate_payment():
    user_id = get_jwt_identity()
    data = request.get_json()
    order_id = data.get('order_id')

    order = orders_db.get(order_id) # Access orders_db

    if not order or order['user_id'] != user_id:
        return jsonify({"msg": "Order not found or does not belong to user"}), 404

    if order['payment_status'] != 'pending' or order['status'] != 'pending_payment':
        return jsonify({"msg": "Payment for this order is already processed or is not pending"}), 400

    # --- Simulate Payment Gateway Interaction ---
    try:
        # In a real app, call payment gateway API (e.g., Stripe, PayPal)
        # Simulate success response from payment gateway
        simulated_payment_intent_id = f"pi_{str(uuid.uuid4())[:8]}"
        simulated_client_secret = f"sec_{str(uuid.uuid4())[:8]}_test"

        # Store payment intent ID with the order (optional but good practice)
        order['payment_intent_id'] = simulated_payment_intent_id # Update orders_db

        return jsonify({
            "msg": "Payment initiated",
            "payment_intent_id": simulated_payment_intent_id,
            "client_secret": simulated_client_secret
        }), 200

    except Exception as e:
        print(f"Simulated Payment Initiation Failed: {e}")
        return jsonify({"msg": "Failed to initiate payment", "error": str(e)}), 500


@app.route('/api/checkout/payment-webhook', methods=['POST'])
# No authentication required for webhooks, secured by verifying signature (simulated)
def payment_webhook():
    # In a real app: Verify signature, parse event, handle types.
    # We will expect a simple JSON payload containing an order_id or payment_intent_id for this sim.
    try:
        event_data = request.get_json()
        simulated_payment_success = event_data.get('type') == 'payment_intent.succeeded' # Simulate event type

        if not simulated_payment_success:
             return jsonify({"msg": "Event type ignored"}), 200

        # Simulate extracting the order_id or payment_intent_id from the payload
        order_id_from_webhook = event_data.get('data', {}).get('object', {}).get('metadata', {}).get('order_id')
        simulated_payment_intent_id = event_data.get('data', {}).get('object', {}).get('id')

        order = None
        if order_id_from_webhook:
            order = orders_db.get(order_id_from_webhook) # Access orders_db
        elif simulated_payment_intent_id:
             order = next((o for o in orders_db.values() if o.get('payment_intent_id') == simulated_payment_intent_id), None) # Access orders_db


        if not order:
            return jsonify({"msg": "Order not found"}), 404

        if order['payment_status'] == 'paid':
            return jsonify({"msg": "Order already paid"}), 200 # Idempotent handling

        # --- Simulate Transaction Start ---
        try:
            # Update order status
            order['payment_status'] = 'paid' # Update orders_db
            order['status'] = 'processing' # Move from pending_payment to processing (Update orders_db)

            # Trigger Order Confirmation Email
            user = users_db.get(order['user_id']) # Access users_db
            if user:
                order_summary_lines = [f"- {item['quantity']} x {products_db.get(item['product_id'],{}).get('title','Unknown Item')} @ ${item['price_at_purchase']:.2f} each" for item in order['items']] # Access products_db
                order_summary = "\n".join(order_summary_lines)

                send_email_notification(
                    recipient_email=user['email'],
                    subject=f"Your Order #{order['id']} Confirmed!",
                    body=f"Thank you for your order! Your order #{order['id']} has been confirmed and is now being processed.\n\n"
                         f"Shipping Address:\n{order['shipping_address']}\n\n"
                         f"Order Summary:\n{order_summary}\n\n"
                         f"Total: ${order['total_amount']:.2f}\n\n"
                         f"You can view your order details here: [Link to Order History]" # Placeholder link
                )

            # --- Simulate Transaction Commit ---
            return jsonify({"msg": "Webhook received and processed successfully"}), 200

        except Exception as e:
            # --- Simulate Transaction Rollback ---
            # In a real DB, rollback changes.
            print(f"Webhook Error processing event and updating DB: {e}. Simulating rollback.")
            return jsonify({"msg": "Error processing webhook"}), 500 # Return 500 for retries


    except Exception as e:
        print(f"Webhook Error parsing request or finding order: {e}")
        return jsonify({"msg": "Error processing webhook request"}), 400


# Customer Order History Endpoints (Engineer 3)

@app.route('/api/customer/orders', methods=['GET'])
@customer_required
def get_customer_orders():
    user_id = get_jwt_identity()
    customer_orders = [order for order in orders_db.values() if order['user_id'] == user_id] # Access orders_db

    # Format orders for response
    formatted_orders = []
    for order in customer_orders:
        formatted_orders.append({
            "order_id": order['id'],
            "order_date": order['order_date'],
            "total_amount": order['total_amount'],
            "status": order['status'],
            "payment_status": order['payment_status'],
            "item_count": sum(item['quantity'] for item in order['items']),
             "preview_items": [ # Include a few item titles for preview
                 products_db.get(item['product_id'],{}).get('title','?') # Access products_db
                 for item in order['items'][:2] # Take first 2 items
             ],
             "has_tracking": order.get('tracking_number') is not None
        })

    # Sort by date, newest first
    formatted_orders.sort(key=lambda x: x['order_date'], reverse=True)

    return jsonify(formatted_orders), 200

@app.route('/api/customer/orders/<order_id>', methods=['GET'])
@customer_required
def get_customer_order_details(order_id):
    user_id = get_jwt_identity()
    order = orders_db.get(order_id) # Access orders_db

    # Ensure the order exists and belongs to the logged-in customer
    if not order or order['user_id'] != user_id:
        return jsonify({"msg": "Order not found or does not belong to this customer"}), 404

    # Fetch product details for order items
    detailed_items = []
    for item in order['items']:
         product = products_db.get(item['product_id']) # Access products_db
         detailed_items.append({
             "product_id": item['product_id'],
             "title": product['title'] if product else 'Unknown Product',
             "quantity": item['quantity'],
             "price_at_purchase": item['price_at_purchase'],
             "image_url": product['image_urls'][0] if product and product['image_urls'] else None
         })

    # Format the order details for response
    order_details = {
        "order_id": order['id'],
        "order_date": order['order_date'],
        "total_amount": order['total_amount'],
        "shipping_address": order['shipping_address'],
        "status": order['status'],
        "payment_status": order['payment_status'],
        "tracking_number": order.get('tracking_number'), # Include tracking if exists
        "items": detailed_items
    }

    return jsonify(order_details), 200

# Product Reviews & Ratings Endpoints (Engineer 3)

@app.route('/api/products/<product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    # Authentication not strictly required for *viewing* reviews
    product = products_db.get(product_id) # Access products_db
    if not product or product.get('status') != 'active':
        return jsonify({"msg": "Product not found or not available for review"}), 404

    product_reviews = [
        {
            "id": review_id,
            "user_id": review['user_id'],
            "rating": review['rating'],
            "comment": review['comment'],
            "review_date": review['review_date'],
            "customer_name": users_db.get(review['user_id'], {}).get('profile', {}).get('name', 'Anonymous User') # Get reviewer name (Access users_db)
        }
        for review_id, review in reviews_db.items() if review['product_id'] == product_id # Access reviews_db
    ]

    # Sort by date, newest first
    product_reviews.sort(key=lambda x: x['review_date'], reverse=True)

    return jsonify(product_reviews), 200


@app.route('/api/products/<product_id>/reviews', methods=['POST'])
@customer_required # Only logged-in customers can leave reviews
def submit_product_review(product_id):
    user_id = get_jwt_identity()
    product = products_db.get(product_id) # Access products_db
    if not product or product.get('status') != 'active':
        return jsonify({"msg": "Product not found or not active"}), 404

    data = request.get_json()
    rating = data.get('rating')
    comment = data.get('comment', '').strip() # Allow empty comments, strip whitespace

    # Validate input
    if not isinstance(rating, int) or not 1 <= rating <= 5:
        return jsonify({"msg": "Rating must be an integer between 1 and 5"}), 400

    # --- Check if user has purchased the product (Crucial Business Logic) ---
    # In a real app, query orders_db and order_items_db using SQLAlchemy/ORM
    has_purchased = False
    for order in orders_db.values(): # Access orders_db
        if order['user_id'] == user_id and order['status'] in ['delivered', 'completed', 'shipped']: # Allow review after shipped or delivered/completed
            for item in order['items']:
                if item['product_id'] == product_id:
                    has_purchased = True
                    break
        if has_purchased:
            break # Found purchase, no need to check further orders

    if not has_purchased:
         return jsonify({"msg": "You can only review products you have purchased"}), 403 # Forbidden

    # Check if user has already reviewed this product (Optional, but common)
    # For this sim, we'll allow multiple reviews for simplicity, but a real app might disallow.
    # existing_review = next((r for r in reviews_db.values() if r['product_id'] == product_id and r['user_id'] == user_id), None)
    # if existing_review:
    #     return jsonify({"msg": "You have already reviewed this product"}), 409 # Conflict

    # Create the review
    review_id = str(uuid.uuid4())
    new_review = {
        "id": review_id,
        "product_id": product_id,
        "user_id": user_id,
        "rating": rating,
        "comment": comment,
        "review_date": datetime.utcnow().isoformat() + 'Z' # Use actual timestamp
    }
    reviews_db[review_id] = new_review # Update reviews_db

    # In a real app, you might trigger a recalculation of the product's average rating (async task).

    return jsonify({"msg": "Review submitted successfully", "review_id": review_id}), 201


# Seller Order Management Endpoints (Engineer 3)

@app.route('/api/seller/orders', methods=['GET'])
@seller_required
def get_seller_orders():
    user_id = get_jwt_identity() # This is the seller_id
    seller_orders_overview = []
    processed_order_ids = set() # Use a set to avoid adding the same order multiple times

    # Iterate through all orders
    for order_id, order in orders_db.items(): # Access orders_db
        if order_id in processed_order_ids:
             continue # Skip if already processed

        # Check if *any* item in the order belongs to this seller
        contains_seller_products = False
        seller_items_count = 0
        total_for_seller_in_order = 0
        item_summaries = [] # To list seller's items in this order overview

        for item in order['items']:
            # Lookup if not stored with item (more robust if product data changes)
            item_product = products_db.get(item['product_id']) # Access products_db
            item_seller_id = item_product.get('seller_id') if item_product else None

            if item_seller_id == user_id:
                contains_seller_products = True
                seller_items_count += item['quantity']
                total_for_seller_in_order += item['quantity'] * item['price_at_purchase']
                item_summaries.append(f"{item['quantity']}x {item_product.get('title','?') if item_product else '?'}")

        # If the order contains products from this seller, add its overview
        if contains_seller_products:
            customer_name = users_db.get(order['user_id'], {}).get('profile', {}).get('name', 'Unknown Customer') # Access users_db
            seller_orders_overview.append({
                "order_id": order_id,
                "customer_name": customer_name,
                "order_date": order['order_date'],
                "status": order['status'], # Show the overall order status
                "payment_status": order['payment_status'], # Show overall payment status
                "seller_item_count": seller_items_count,
                "seller_order_total": total_for_seller_in_order, # Total amount specifically for this seller's items
                "seller_items_summary": ", ".join(item_summaries),
                 "has_tracking": order.get('tracking_number') is not None # Does the overall order have tracking?
            })
            processed_order_ids.add(order_id)


    # Sort by date, newest first
    seller_orders_overview.sort(key=lambda x: x['order_date'], reverse=True)

    return jsonify(seller_orders_overview), 200


@app.route('/api/seller/orders/<order_id>', methods=['GET'])
@seller_required
def get_seller_order_details(order_id):
    user_id = get_jwt_identity() # This is the seller_id
    order = orders_db.get(order_id) # Access orders_db

    # Ensure the order exists
    if not order:
        return jsonify({"msg": "Order not found"}), 404

    # Check if the order contains any items from the logged-in seller
    seller_specific_items = []
    total_for_seller = 0
    for item in order['items']:
        # Lookup if not stored with item (more robust if product data changes)
        item_product = products_db.get(item['product_id']) # Access products_db
        item_seller_id = item_product.get('seller_id') if item_product else None

        if item_seller_id == user_id:
            seller_specific_items.append(item)
            total_for_seller += item['quantity'] * item['price_at_purchase']


    if not seller_specific_items:
         # If the order exists but has no items from *this* seller, it's a permission issue.
         return jsonify({"msg": "You do not have permission to view details for this order"}), 403

    # Fetch product details for seller's items in this order
    detailed_seller_items = []
    for item in seller_specific_items:
         product = products_db.get(item['product_id']) # Access products_db
         detailed_seller_items.append({
             "product_id": item['product_id'],
             "title": product['title'] if product else 'Unknown Product',
             "quantity": item['quantity'],
             "price_at_purchase": item['price_at_purchase'],
             "image_url": product['image_urls'][0] if product and product['image_urls'] else None
         })

    # Get customer info (only necessary info like shipping address, not sensitive details like email)
    customer = users_db.get(order['user_id']) # Access users_db
    customer_info = {
        "name": customer['profile'].get('name', 'Unknown Customer'),
        "shipping_address": order['shipping_address'] # Use address stored with order
        # Avoid sending customer email or other sensitive info unless necessary and authorized
    }

    # Format the relevant order details for the seller
    seller_order_details = {
        "order_id": order['id'],
        "order_date": order['order_date'],
        "customer_info": customer_info,
        "overall_status": order['status'], # Overall status of the order
        "payment_status": order['payment_status'],
        "tracking_number": order.get('tracking_number'), # Seller can see tracking if added
        "items_from_your_shop": detailed_seller_items, # Only show seller's items
        "total_for_your_shop": total_for_seller # Sum of this seller's items in this order
    }

    return jsonify(seller_order_details), 200


@app.route('/api/seller/orders/<order_id>/status', methods=['PUT'])
@seller_required
def update_seller_order_status(order_id):
    user_id = get_jwt_identity() # This is the seller_id
    order = orders_db.get(order_id) # Access orders_db

    if not order:
        return jsonify({"msg": "Order not found"}), 404

    # Check if the order contains any items from this seller
    contains_seller_products = any(products_db.get(item['product_id'], {}).get('seller_id') == user_id for item in order['items']) # Access products_db

    if not contains_seller_products:
        return jsonify({"msg": "You do not have permission to update this order"}), 403 # Forbidden

    data = request.get_json()
    new_status = data.get('status')
    tracking_number = data.get('tracking_number') # Optional

    # Validate allowed status transitions for seller
    # For V1 spec, seller can mark as shipped. Assume only transition from 'processing' or 'paid' state.
    allowed_target_status = 'shipped' # Only 'shipped' is allowed by seller in V1 spec
    allowed_initial_statuses = ['pending_payment', 'processing', 'paid'] # States from which seller can ship

    if new_status != allowed_target_status:
         return jsonify({"msg": f"Invalid status update. Sellers can only mark orders as '{allowed_target_status}'."}), 400

    if order['status'] not in allowed_initial_statuses:
        # Cannot mark as shipped if not in a state where it can be shipped
        return jsonify({"msg": f"Order status '{order['status']}' cannot be updated to '{allowed_target_status}'."}), 400

    if new_status == 'shipped' and (tracking_number is None or not tracking_number.strip()):
         return jsonify({"msg": "Tracking number is required when marking as 'shipped'."}), 400

    # Prevent marking as shipped if it's already shipped or later
    if order['status'] in ['shipped', 'delivered', 'cancelled', 'refunded']:
         return jsonify({"msg": f"Order is already in status '{order['status']}'."}), 400


    # --- Simulate Transaction Start ---
    try:
        # Update the overall order status
        order['status'] = new_status # Update orders_db
        order['tracking_number'] = tracking_number # Store tracking (Update orders_db)

        # --- Simulate Transaction Commit ---

        # Trigger Shipping Notification Email if status is 'shipped'
        if new_status == 'shipped':
            customer = users_db.get(order['user_id']) # Access users_db
            if customer:
                 # Build a list of the seller's items in this order for the email
                 seller_items_in_order = [
                      item for item in order['items']
                      if products_db.get(item['product_id'], {}).get('seller_id') == user_id # Access products_db
                 ]
                 item_list_str = "\n".join([f"- {item['quantity']} x {products_db.get(item['product_id'],{}).get('title','Unknown Item')}" for item in seller_items_in_order]) # Access products_db
                 seller_shop_name = users_db.get(user_id,{}).get('profile',{}).get('shop_name', 'a seller') # Access users_db

                 send_email_notification(
                     recipient_email=customer['email'],
                     subject=f"Your Order #{order_id} Has Shipped From {seller_shop_name}!",
                     body=f"Good news! Items from your order #{order_id} from {seller_shop_name} have shipped.\n\n"
                          f"Items Shipped from this seller:\n{item_list_str}\n\n"
                          f"Tracking Number: {tracking_number}\n\n"
                          f"You can view your order details here: [Link to Order History]" # Placeholder link
                 )

        return jsonify({"msg": f"Order status updated to '{new_status}'", "order_id": order_id, "status": new_status, "tracking_number": tracking_number}), 200

    except Exception as e:
        # --- Simulate Transaction Rollback ---
        # In a real app, rollback DB changes
        print(f"Error updating order status: {e}. Simulating rollback.")
        return jsonify({"msg": "Failed to update order status", "error": str(e)}), 500


# Admin Order Management Endpoints (Engineer 3)
# Note: Admin endpoints might be split among engineers based on the data they manage,
# but order management is primarily Engineer 3's domain per the plan.

@app.route('/api/admin/orders', methods=['GET'])
@admin_required
def admin_get_all_orders():
    # Return all orders, potentially with pagination/filtering (not implemented in basic sim)
    all_orders = list(orders_db.values()) # Access orders_db

    # Format for overview
    formatted_orders = []
    for order in all_orders:
         customer_name = users_db.get(order['user_id'], {}).get('profile', {}).get('name', 'Unknown Customer') # Access users_db
         formatted_orders.append({
             "order_id": order['id'],
             "customer_id": order['user_id'], # Admin can see customer ID
             "customer_name": customer_name,
             "order_date": order['order_date'],
             "total_amount": order['total_amount'],
             "status": order['status'],
             "payment_status": order['payment_status'],
             "item_count": sum(item['quantity'] for item in order['items']),
             "has_tracking": order.get('tracking_number') is not None
         })

    # Sort by date, newest first
    formatted_orders.sort(key=lambda x: x['order_date'], reverse=True)

    return jsonify(formatted_orders), 200


@app.route('/api/admin/orders/<order_id>', methods=['GET'])
@admin_required
def admin_get_order_details(order_id):
    order = orders_db.get(order_id) # Access orders_db

    if not order:
        return jsonify({"msg": "Order not found"}), 404

    # Fetch details for all items in the order
    detailed_items = []
    for item in order['items']:
         product = products_db.get(item['product_id']) # Access products_db
         # Lookup seller details for each item's seller
         item_seller = users_db.get(item.get('seller_id')) # Use seller_id from item first (Access users_db)
         if not item_seller and product: # Fallback lookup via product if seller_id not stored on item (Access users_db)
              item_seller = users_db.get(product.get('seller_id'))

         detailed_items.append({
             "product_id": item['product_id'],
             "title": product['title'] if product else 'Unknown Product',
             "quantity": item['quantity'],
             "price_at_purchase": item['price_at_purchase'],
             "seller_id": item_seller['id'] if item_seller else 'Unknown',
             "seller_shop_name": item_seller['profile'].get('shop_name', 'Unknown Seller') if item_seller else 'Unknown Seller',
             "image_url": product['image_urls'][0] if product and product['image_urls'] else None
         })

    # Get customer info
    customer = users_db.get(order['user_id']) # Access users_db
    customer_info = {
        "id": order['user_id'],
        "name": customer['profile'].get('name', 'Unknown Customer'),
        "email": customer.get('email'), # Admin can see customer email
        "shipping_address": order['shipping_address']
    }

    # Format the full order details for the admin
    full_order_details = {
        "order_id": order['id'],
        "order_date": order['order_date'],
        "customer_info": customer_info,
        "total_amount": order['total_amount'],
        "status": order['status'],
        "payment_status": order['payment_status'],
        "tracking_number": order.get('tracking_number'),
        "items": detailed_items
    }

    return jsonify(full_order_details), 200

@app.route('/api/admin/orders/<order_id>/status', methods=['PUT'])
@admin_required
def admin_update_order_status(order_id):
    order = orders_db.get(order_id) # Access orders_db

    if not order:
        return jsonify({"msg": "Order not found"}), 404

    data = request.get_json()
    new_status = data.get('status')
    tracking_number = data.get('tracking_number') # Admin can also update tracking

    # Validate allowed status transitions for admin (Admin can set pretty much any status)
    allowed_statuses = ['pending_payment', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded']
    if new_status not in allowed_statuses:
         return jsonify({"msg": f"Invalid status '{new_status}'"}), 400

    # --- Simulate Transaction Start ---
    try:
        # Store old status for comparison
        old_status = order['status']

        # Update the overall order status
        order['status'] = new_status # Update orders_db
        # Admin can explicitly set tracking number (including None)
        if 'tracking_number' in data: # Check if key is present
             order['tracking_number'] = tracking_number # Update orders_db

        # Admin might also update payment_status directly
        if 'payment_status' in data: # Check if key is present
             # Validate payment status if needed
             allowed_payment_statuses = ['pending', 'paid', 'failed', 'refunded']
             if data['payment_status'] not in allowed_payment_statuses:
                  return jsonify({"msg": f"Invalid payment status '{data['payment_status']}'"}), 400
             order['payment_status'] = data['payment_status'] # Update orders_db


        # --- Simulate Transaction Commit ---

        # Trigger Notification Emails based on status changes (if needed for admin changes)
        customer = users_db.get(order['user_id']) # Access users_db
        if customer and new_status != old_status: # Only send if status actually changed
             subject = f"Update on Your Order #{order_id}"
             body = f"The status of your order #{order_id} has been updated to '{new_status}'.\n\n"
             # Add status-specific details to the email body
             if new_status == 'cancelled':
                  body += "Your order has been cancelled."
             elif new_status == 'refunded':
                  body += "A refund has been processed for your order."
             elif new_status == 'shipped':
                  body += f"Your order has been shipped!\nTracking Number: {order.get('tracking_number', 'N/A')}"
             elif new_status == 'delivered':
                 body += "Your order has been marked as delivered."
             else:
                 body += f"Current Status: {new_status}" # Generic update

             body += "\n\nYou can view your order details here: [Link to Order History]" # Placeholder link

             send_email_notification(
                 recipient_email=customer['email'],
                 subject=subject,
                 body=body
             )
        elif customer and 'payment_status' in data and data['payment_status'] != order.get('payment_status'): # Notify if payment status changed by admin AND status didn't trigger email
             if new_status == old_status: # Only if status didn't change
                  send_email_notification(
                      recipient_email=customer['email'],
                      subject=f"Payment Status Update for Order #{order_id}",
                      body=f"The payment status for your order #{order_id} has been updated to '{order['payment_status']}'.\n\n"
                           f"You can view your order details here: [Link to Order History]" # Placeholder link
                  )


        return jsonify({"msg": f"Order status updated to '{new_status}'", "order_id": order_id, "status": new_status, "tracking_number": order.get('tracking_number'), "payment_status": order['payment_status']}), 200

    except Exception as e:
        # --- Simulate Transaction Rollback ---
        # In a real app, rollback DB changes
        print(f"Error updating order status by admin: {e}. Simulating rollback.")
        return jsonify({"msg": "Failed to update order status", "error": str(e)}), 500

# --- Basic Simulated Login for Testing This File in Isolation ---
# In a real project, Engineer 1 would provide the actual /api/login endpoint.
# This is included here solely to make this single file runnable for testing Engineer 3's routes.
# This endpoint would be part of Engineer 1's code.
@app.route('/sim_login', methods=['POST'])
def sim_login():
    """Simulates login for testing purposes."""
    data = request.get_json()
    email = data.get('email')
    # In a real app, you'd verify password hash
    user = next((u for u in users_db.values() if u.get('email') == email), None)
    if user:
        # Use user ID as identity in the token
        access_token = create_access_token(identity=user['id'])
        return jsonify(access_token=access_token, user_id=user['id'], role=user['role'])
    return jsonify({"msg": "Bad email or password"}), 401


# --- Main application entry point (if this were the main file) ---
# This block would be handled by Engineer 1 in the final integrated application.
if __name__ == '__main__':
    # Engineer 1 would configure the database and start the app.
    # db.create_all() # Example if using SQLAlchemy
    # Add dummy data if needed for initial testing
    print("Running simulated Flask app for Engineer 3's features.")
    print("\nNOTE: This is a simplified simulation using in-memory dictionaries.")
    print("It does NOT use a real database, persistent storage, or proper security like password hashing.")
    print("Authentication is simulated with JWT based on user ID lookup.")
    print("Payment Gateway interaction and Webhooks are simulated using print statements.")
    print("\nTo test endpoints:")
    print("1. Run this script.")
    print("2. Get a JWT token using the /sim_login endpoint (POST with {'email': 'user_email'}).")
    print("   Example emails: customer1@example.com, seller1@example.com, admin1@example.com, seller2@example.com, customer2@example.com")
    print("3. Include the token in the 'Authorization: Bearer <token>' header for authenticated endpoints.")
    print("\nEngineer 3 Endpoints Implemented:")
    print("  GET /api/cart")
    print("  POST /api/cart")
    print("  PUT /api/cart/<product_id>")
    print("  DELETE /api/cart/<product_id>")
    print("  POST /api/checkout/create-order")
    print("  POST /api/checkout/initiate-payment")
    print("  POST /api/checkout/payment-webhook (Simulated - Requires specific JSON payload e.g. {'type': 'payment_intent.succeeded', 'data': {'object': {'id': 'sim_pi_id', 'metadata': {'order_id': 'order_id'}} } })")
    print("  GET /api/customer/orders")
    print("  GET /api/customer/orders/<order_id>")
    print("  GET /api/products/<product_id>/reviews")
    print("  POST /api/products/<product_id>/reviews")
    print("  GET /api/seller/orders")
    print("  GET /api/seller/orders/<order_id>")
    print("  PUT /api/seller/orders/<order_id>/status")
    print("  GET /api/admin/orders")
    print("  GET /api/admin/orders/<order_id>")
    print("  PUT /api/admin/orders/<order_id>/status")

    app.run(debug=True, port=5000)
