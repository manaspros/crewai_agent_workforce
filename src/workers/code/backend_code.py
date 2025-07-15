import json
import os
from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

tokens = {}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default='buyer')
    addresses = db.relationship('Address', backref='user', lazy=True)
    orders = db.relationship('Order', backref='buyer', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    seller_profile = db.relationship('SellerProfile', back_populates='user', uselist=False, foreign_keys='SellerProfile.user_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class SellerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    shop_name = db.Column(db.String(120), nullable=False)
    shop_description = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)
    products = db.relationship('Product', backref='seller', lazy=True)
    user = db.relationship('User', back_populates='seller_profile', uselist=False, foreign_keys=[user_id])

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100))
    zip = db.Column(db.String(20))
    country = db.Column(db.String(100), nullable=False)
    is_default = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller_profile.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    is_approved = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(255))
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shipping_address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    tracking_number = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)
    shipping_address = db.relationship('Address', backref='orders_as_shipping', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def authenticate_token(token):
    user_id = tokens.get(token)
    if user_id:
        user = User.query.get(user_id)
        return user
    return None

def generate_token(user_id):
    token = secrets.token_hex(16)
    tokens[token] = user_id
    return token

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"message": "Authorization header missing"}), 401
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                return jsonify({"message": "Invalid authentication scheme"}), 401
            user = authenticate_token(token)
            if not user:
                return jsonify({"message": "Invalid or expired token"}), 401
            g.current_user = user
        except ValueError:
             return jsonify({"message": "Invalid Authorization header format"}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.current_user.role != required_role and g.current_user.role != 'admin':
                 return jsonify({"message": "Unauthorized"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
     return role_required('admin')(f)

def seller_required(f):
     return role_required('seller')(f)

with app.app_context():
    db.create_all()

    if not User.query.filter_by(email='admin@example.com').first():
        admin_user = User(email='admin@example.com', role='admin')
        admin_user.set_password('adminpassword')
        db.session.add(admin_user)
        db.session.commit()

    if not User.query.filter_by(email='seller@example.com').first():
        seller_user = User(email='seller@example.com', role='seller')
        seller_user.set_password('sellerpassword')
        db.session.add(seller_user)
        db.session.commit()
        seller_profile = SellerProfile(user_id=seller_user.id, shop_name='Artisan Shop', shop_description='Handmade goods.', is_approved=True)
        db.session.add(seller_profile)
        db.session.commit()
        if not Product.query.filter_by(seller_id=seller_profile.id).first():
             product1 = Product(seller_id=seller_profile.id, name='Handmade Mug', description='A beautiful ceramic mug.', price=18.50, stock=10, is_approved=True, image_url='https://via.placeholder.com/180x120?text=Mug')
             product2 = Product(seller_id=seller_profile.id, name='Wooden Coasters (Set of 4)', description='Set of 4 engraved wooden coasters.', price=25.00, stock=15, is_approved=True, image_url='https://via.placeholder.com/180x120?text=Coasters')
             product3 = Product(seller_id=seller_profile.id, name='Knitted Scarf', description='Soft wool knitted scarf.', price=35.00, stock=5, is_approved=True, image_url='https://via.placeholder.com/180x120?text=Scarf')
             db.session.add_all([product1, product2, product3])
             db.session.commit()


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'buyer')
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409
    user = User(email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "user_id": user.id}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401
    token = generate_token(user.id)
    return jsonify({"token": token, "user_id": user.id, "role": user.role}), 200

@app.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    if g.current_user.id != user.id and g.current_user.role != 'admin':
         return jsonify({"message": "Unauthorized"}), 403
    seller_info = None
    if user.role == 'seller' and user.seller_profile:
        seller_info = {
            "id": user.seller_profile.id,
            "shop_name": user.seller_profile.shop_name,
            "shop_description": user.seller_profile.shop_description,
            "is_approved": user.seller_profile.is_approved
        }
    return jsonify({
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "seller_profile": seller_info
    }), 200

@app.route('/users/<int:user_id>/addresses', methods=['GET'])
@login_required
def get_user_addresses(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    if g.current_user.id != user.id and g.current_user.role != 'admin':
         return jsonify({"message": "Unauthorized"}), 403
    addresses = Address.query.filter_by(user_id=user.id).all()
    return jsonify([{
        "id": addr.id,
        "street": addr.street,
        "city": addr.city,
        "state": addr.state,
        "zip": addr.zip,
        "country": addr.country,
        "is_default": addr.is_default
    } for addr in addresses]), 200

@app.route('/users/<int:user_id>/addresses', methods=['POST'])
@login_required
def add_user_address(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    if g.current_user.id != user.id:
         return jsonify({"message": "Unauthorized"}), 403
    data = request.get_json()
    street = data.get('street')
    city = data.get('city')
    state = data.get('state')
    zip = data.get('zip')
    country = data.get('country')
    if not street or not city or not country:
         return jsonify({"message": "Street, city, and country are required"}), 400

    # Make this the default if it's the first address
    is_default = data.get('is_default', False)
    if is_default:
        current_default = Address.query.filter_by(user_id=user.id, is_default=True).first()
        if current_default:
            current_default.is_default = False

    address = Address(user_id=user.id, street=street, city=city, state=state, zip=zip, country=country, is_default=is_default or not bool(Address.query.filter_by(user_id=user.id).first()))
    db.session.add(address)
    db.session.commit()
    return jsonify({"message": "Address added", "address_id": address.id}), 201

@app.route('/addresses/<int:address_id>', methods=['PUT'])
@login_required
def update_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        return jsonify({"message": "Address not found"}), 404
    if address.user_id != g.current_user.id:
        return jsonify({"message": "Unauthorized"}), 403
    data = request.get_json()
    address.street = data.get('street', address.street)
    address.city = data.get('city', address.city)
    address.state = data.get('state', address.state)
    address.zip = data.get('zip', address.zip)
    address.country = data.get('country', address.country)

    is_default = data.get('is_default')
    if is_default is not None and is_default:
        current_default = Address.query.filter_by(user_id=g.current_user.id, is_default=True).first()
        if current_default:
            current_default.is_default = False
        address.is_default = True
    elif is_default is not None and not is_default and address.is_default:
         # Prevent removing default if it's the only address
         if Address.query.filter_by(user_id=g.current_user.id).count() > 1:
             address.is_default = False


    db.session.commit()
    return jsonify({"message": "Address updated"}), 200

@app.route('/addresses/<int:address_id>', methods=['DELETE'])
@login_required
def delete_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        return jsonify({"message": "Address not found"}), 404
    if address.user_id != g.current_user.id:
        return jsonify({"message": "Unauthorized"}), 403
    if address.is_default and Address.query.filter_by(user_id=g.current_user.id).count() > 1:
        return jsonify({"message": "Cannot delete default address if others exist. Set a new default first."}), 400

    db.session.delete(address)
    db.session.commit()
    # If the deleted address was the only one, no default is needed. If others exist,
    # and this wasn't the default (handled above), or this was the last one, it's fine.
    if Address.query.filter_by(user_id=g.current_user.id, is_default=True).first() is None and \
       Address.query.filter_by(user_id=g.current_user.id).first() is not None:
           first_address = Address.query.filter_by(user_id=g.current_user.id).first()
           first_address.is_default = True
           db.session.commit()


    return jsonify({"message": "Address deleted"}), 200


@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.filter_by(is_approved=True).all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "stock": p.stock,
        "image_url": p.image_url,
        "seller_id": p.seller_id,
        "seller_shop_name": p.seller.shop_name if p.seller else None
    } for p in products]), 200

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_detail(product_id):
    product = Product.query.get(product_id)
    if not product or not product.is_approved:
        return jsonify({"message": "Product not found or not approved"}), 404

    reviews = Review.query.filter_by(product_id=product.id).all()
    review_list = [{
        "id": r.id,
        "rating": r.rating,
        "comment": r.comment,
        "user_email": r.user.email if r.user else 'Anonymous',
        "created_at": r.created_at.isoformat()
    } for r in reviews]

    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "image_url": product.image_url,
        "seller_id": product.seller_id,
        "seller_shop_name": product.seller.shop_name if product.seller else None,
        "reviews": review_list
    }), 200

@app.route('/products', methods=['POST'])
@seller_required
def create_product():
    if not g.current_user.seller_profile or not g.current_user.seller_profile.is_approved:
         return jsonify({"message": "User is not an approved seller"}), 403

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock', 0)
    image_url = data.get('image_url')

    if not name or price is None:
        return jsonify({"message": "Name and price are required"}), 400
    try:
        price = float(price)
        stock = int(stock)
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid price or stock format"}), 400

    product = Product(
        seller_id=g.current_user.seller_profile.id,
        name=name,
        description=description,
        price=price,
        stock=stock,
        image_url=image_url,
        is_approved=False # Requires admin approval
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product created, awaiting admin approval", "product_id": product.id}), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
@seller_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    if product.seller_id != g.current_user.seller_profile.id:
         return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    product.image_url = data.get('image_url', product.image_url)

    # Update requires re-approval
    product.is_approved = False

    db.session.commit()
    return jsonify({"message": "Product updated, re-awaiting admin approval"}), 200

@app.route('/products/<int:product_id>', methods=['DELETE'])
@seller_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    if product.seller_id != g.current_user.seller_profile.id:
         return jsonify({"message": "Unauthorized"}), 403

    # Basic check: don't delete if in active carts or orders
    if CartItem.query.filter_by(product_id=product.id).first() or \
       OrderItem.query.filter_by(product_id=product.id).first():
        return jsonify({"message": "Cannot delete product with associated cart items or orders"}), 400

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200

@app.route('/cart', methods=['GET'])
@login_required
def get_cart():
    cart_items = CartItem.query.filter_by(user_id=g.current_user.id).all()
    items_list = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            items_list.append({
                "id": item.id,
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": item.quantity,
                "image_url": product.image_url
            })
        else:
             db.session.delete(item)
             db.session.commit()

    return jsonify(items_list), 200

@app.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    if not product_id or quantity <= 0:
        return jsonify({"message": "Valid product_id and quantity required"}), 400

    product = Product.query.get(product_id)
    if not product or not product.is_approved:
        return jsonify({"message": "Product not found or not approved"}), 404
    if product.stock < quantity:
        return jsonify({"message": f"Not enough stock. Only {product.stock} available."}), 400

    cart_item = CartItem.query.filter_by(user_id=g.current_user.id, product_id=product_id).first()
    if cart_item:
        if product.stock < cart_item.quantity + quantity:
             return jsonify({"message": f"Adding {quantity} exceeds stock. Only {product.stock - cart_item.quantity} more available."}), 400
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=g.current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({"message": "Item added to cart"}), 200

@app.route('/cart/update/<int:item_id>', methods=['PUT'])
@login_required
def update_cart_item(item_id):
    data = request.get_json()
    quantity = data.get('quantity')
    if quantity is None or quantity <= 0:
        return jsonify({"message": "Valid quantity required"}), 400

    cart_item = CartItem.query.filter_by(id=item_id, user_id=g.current_user.id).first()
    if not cart_item:
        return jsonify({"message": "Cart item not found"}), 404

    product = Product.query.get(cart_item.product_id)
    if not product:
         db.session.delete(cart_item)
         db.session.commit()
         return jsonify({"message": "Product for this cart item not found or removed, item deleted"}), 404

    if product.stock < quantity:
        return jsonify({"message": f"Not enough stock. Only {product.stock} available."}), 400

    cart_item.quantity = quantity
    db.session.commit()
    return jsonify({"message": "Cart item updated"}), 200

@app.route('/cart/remove/<int:item_id>', methods=['DELETE'])
@login_required
def remove_cart_item(item_id):
    cart_item = CartItem.query.filter_by(id=item_id, user_id=g.current_user.id).first()
    if not cart_item:
        return jsonify({"message": "Cart item not found"}), 404
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Cart item removed"}), 200

@app.route('/orders', methods=['POST'])
@login_required
def create_order():
    data = request.get_json()
    shipping_address_id = data.get('shipping_address_id')
    if not shipping_address_id:
        return jsonify({"message": "Shipping address is required"}), 400

    shipping_address = Address.query.filter_by(id=shipping_address_id, user_id=g.current_user.id).first()
    if not shipping_address:
        return jsonify({"message": "Shipping address not found or does not belong to user"}), 404

    cart_items = CartItem.query.filter_by(user_id=g.current_user.id).all()
    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    total_amount = 0
    order_items_to_add = []
    products_to_update = {}

    for item in cart_items:
        product = Product.query.get(item.product_id)
        if not product or not product.is_approved or product.stock < item.quantity:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": f"Product '{product.name if product else item.product_id}' unavailable or not enough stock. Please review cart."}), 400
        order_items_to_add.append(OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price_at_purchase=product.price
        ))
        total_amount += product.price * item.quantity
        if product.id not in products_to_update:
            products_to_update[product.id] = product
        products_to_update[product.id].stock -= item.quantity

    new_order = Order(
        user_id=g.current_user.id,
        shipping_address_id=shipping_address.id,
        total_amount=total_amount,
        status='pending', # Or 'processing' after payment sim
        created_at=datetime.utcnow()
    )
    db.session.add(new_order)
    db.session.flush() # Assigns ID to new_order

    for item in order_items_to_add:
        item.order_id = new_order.id
        db.session.add(item)

    # Simulate payment success
    new_order.status = 'processing'

    # Clear cart
    for item in cart_items:
        db.session.delete(item)

    db.session.commit()
    return jsonify({"message": "Order created successfully", "order_id": new_order.id, "status": new_order.status}), 201

@app.route('/users/<int:user_id>/orders', methods=['GET'])
@login_required
def get_user_orders(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    if g.current_user.id != user.id and g.current_user.role != 'admin':
         return jsonify({"message": "Unauthorized"}), 403

    orders = Order.query.filter_by(user_id=user.id).all()
    orders_list = []
    for order in orders:
        items_list = []
        for item in order.items:
            product = Product.query.get(item.product_id)
            items_list.append({
                "product_id": item.product_id,
                "product_name": product.name if product else 'Unknown Product',
                "quantity": item.quantity,
                "price_at_purchase": item.price_at_purchase,
                "image_url": product.image_url if product else None
            })
        orders_list.append({
            "id": order.id,
            "total_amount": order.total_amount,
            "status": order.status,
            "tracking_number": order.tracking_number,
            "created_at": order.created_at.isoformat(),
            "items": items_list
        })
    return jsonify(orders_list), 200

@app.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order_detail(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    # Check if user is the buyer, a seller of items in the order, or an admin
    is_buyer = order.user_id == g.current_user.id
    is_seller = False
    if g.current_user.role == 'seller' and g.current_user.seller_profile:
         seller_product_ids = [p.id for p in Product.query.filter_by(seller_id=g.current_user.seller_profile.id).all()]
         for item in order.items:
             if item.product_id in seller_product_ids:
                 is_seller = True
                 break
    is_admin = g.current_user.role == 'admin'

    if not is_buyer and not is_seller and not is_admin:
        return jsonify({"message": "Unauthorized"}), 403

    items_list = []
    for item in order.items:
        product = Product.query.get(item.product_id)
        items_list.append({
            "product_id": item.product_id,
            "product_name": product.name if product else 'Unknown Product',
            "quantity": item.quantity,
            "price_at_purchase": item.price_at_purchase,
            "image_url": product.image_url if product else None,
            "seller_id": product.seller_id if product else None
        })

    shipping_addr = order.shipping_address
    shipping_address_detail = {
        "street": shipping_addr.street,
        "city": shipping_addr.city,
        "state": shipping_addr.state,
        "zip": shipping_addr.zip,
        "country": shipping_addr.country,
    } if shipping_addr else None


    return jsonify({
        "id": order.id,
        "user_id": order.user_id,
        "user_email": order.buyer.email if order.buyer else 'Unknown User',
        "shipping_address": shipping_address_detail,
        "total_amount": order.total_amount,
        "status": order.status,
        "tracking_number": order.tracking_number,
        "created_at": order.created_at.isoformat(),
        "updated_at": order.updated_at.isoformat(),
        "items": items_list
    }), 200

@app.route('/orders/<int:order_id>/status', methods=['PUT'])
@seller_required
def update_order_status(order_id):
     order = Order.query.get(order_id)
     if not order:
         return jsonify({"message": "Order not found"}), 404

     # Check if the seller sells *any* product in this order
     is_seller_of_this_order = False
     if g.current_user.seller_profile:
        seller_product_ids = [p.id for p in Product.query.filter_by(seller_id=g.current_user.seller_profile.id).all()]
        for item in order.items:
            if item.product_id in seller_product_ids:
                is_seller_of_this_order = True
                break

     if not is_seller_of_this_order and g.current_user.role != 'admin':
          return jsonify({"message": "Unauthorized"}), 403

     data = request.get_json()
     new_status = data.get('status')
     valid_statuses = ['pending', 'processing', 'shipped', 'completed', 'cancelled']
     if new_status not in valid_statuses:
          return jsonify({"message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400

     order.status = new_status
     order.updated_at = datetime.utcnow()
     db.session.commit()
     return jsonify({"message": "Order status updated", "order_id": order.id, "status": order.status}), 200

@app.route('/orders/<int:order_id>/tracking', methods=['PUT'])
@seller_required
def add_order_tracking(order_id):
     order = Order.query.get(order_id)
     if not order:
         return jsonify({"message": "Order not found"}), 404

     # Check if the seller sells *any* product in this order
     is_seller_of_this_order = False
     if g.current_user.seller_profile:
        seller_product_ids = [p.id for p in Product.query.filter_by(seller_id=g.current_user.seller_profile.id).all()]
        for item in order.items:
            if item.product_id in seller_product_ids:
                is_seller_of_this_order = True
                break

     if not is_seller_of_this_order and g.current_user.role != 'admin':
          return jsonify({"message": "Unauthorized"}), 403

     data = request.get_json()
     tracking_number = data.get('tracking_number')

     order.tracking_number = tracking_number
     order.updated_at = datetime.utcnow()
     # Automatically set status to shipped if tracking is added and status is processing/pending
     if tracking_number and order.status in ['pending', 'processing']:
         order.status = 'shipped'
     db.session.commit()
     return jsonify({"message": "Order tracking updated", "order_id": order.id, "tracking_number": order.tracking_number}), 200

@app.route('/products/<int:product_id>/reviews', methods=['POST'])
@login_required
def add_review(product_id):
    if g.current_user.role != 'buyer':
        return jsonify({"message": "Only buyers can leave reviews"}), 403

    product = Product.query.get(product_id)
    if not product or not product.is_approved:
        return jsonify({"message": "Product not found or not approved"}), 404

    # Check if the buyer has purchased this product
    has_purchased = OrderItem.query.join(Order).\
        filter(Order.user_id == g.current_user.id, OrderItem.product_id == product.id).\
        count() > 0

    if not has_purchased:
         return jsonify({"message": "You can only review products you have purchased"}), 403

    data = request.get_json()
    rating = data.get('rating')
    comment = data.get('comment')

    if rating is None or not (1 <= int(rating) <= 5):
        return jsonify({"message": "Rating must be an integer between 1 and 5"}), 400

    existing_review = Review.query.filter_by(user_id=g.current_user.id, product_id=product_id).first()
    if existing_review:
         return jsonify({"message": "You have already reviewed this product"}), 409

    review = Review(
        product_id=product_id,
        user_id=g.current_user.id,
        rating=int(rating),
        comment=comment,
        created_at=datetime.utcnow()
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review added", "review_id": review.id}), 201

@app.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    product = Product.query.get(product_id)
    if not product or not product.is_approved:
        return jsonify({"message": "Product not found or not approved"}), 404
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify([{
        "id": r.id,
        "rating": r.rating,
        "comment": r.comment,
        "user_email": r.user.email if r.user else 'Anonymous',
        "created_at": r.created_at.isoformat()
    } for r in reviews]), 200

@app.route('/seller/apply', methods=['POST'])
@login_required
def apply_seller():
    if g.current_user.role != 'buyer':
        return jsonify({"message": "Only existing buyers can apply to be sellers"}), 400
    if g.current_user.seller_profile:
        return jsonify({"message": "User already has a seller profile"}), 409

    data = request.get_json()
    shop_name = data.get('shop_name')
    shop_description = data.get('shop_description')
    if not shop_name:
        return jsonify({"message": "Shop name is required"}), 400

    seller_profile = SellerProfile(
        user_id=g.current_user.id,
        shop_name=shop_name,
        shop_description=shop_description,
        is_approved=False # Requires admin approval
    )
    db.session.add(seller_profile)
    g.current_user.role = 'seller' # Temporarily change role, approval needed
    g.current_user.seller_profile = seller_profile
    db.session.commit()
    return jsonify({"message": "Seller application submitted, awaiting admin approval", "seller_profile_id": seller_profile.id}), 201

@app.route('/seller/me', methods=['GET'])
@seller_required
def get_my_seller_profile():
    seller_profile = g.current_user.seller_profile
    if not seller_profile:
         return jsonify({"message": "Seller profile not found"}), 404
    return jsonify({
        "id": seller_profile.id,
        "user_id": seller_profile.user_id,
        "shop_name": seller_profile.shop_name,
        "shop_description": seller_profile.shop_description,
        "is_approved": seller_profile.is_approved
    }), 200

@app.route('/seller/me', methods=['PUT'])
@seller_required
def update_my_seller_profile():
    seller_profile = g.current_user.seller_profile
    if not seller_profile:
         return jsonify({"message": "Seller profile not found"}), 404
    data = request.get_json()
    seller_profile.shop_name = data.get('shop_name', seller_profile.shop_name)
    seller_profile.shop_description = data.get('shop_description', seller_profile.shop_description)
    db.session.commit()
    return jsonify({"message": "Seller profile updated"}), 200

@app.route('/seller/<int:seller_id>/products', methods=['GET'])
def get_seller_products(seller_id):
    seller = SellerProfile.query.get(seller_id)
    if not seller or not seller.is_approved:
        return jsonify({"message": "Seller not found or not approved"}), 404
    products = Product.query.filter_by(seller_id=seller_id, is_approved=True).all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "stock": p.stock,
        "image_url": p.image_url,
        "seller_id": p.seller_id,
        "seller_shop_name": p.seller.shop_name if p.seller else None
    } for p in products]), 200

@app.route('/seller/me/orders', methods=['GET'])
@seller_required
def get_seller_orders():
    if not g.current_user.seller_profile or not g.current_user.seller_profile.is_approved:
         return jsonify({"message": "User is not an approved seller"}), 403

    seller_product_ids = [p.id for p in Product.query.filter_by(seller_id=g.current_user.seller_profile.id).all()]

    # Find all order items belonging to the seller's products
    seller_order_items = OrderItem.query.filter(OrderItem.product_id.in_(seller_product_ids)).all()

    # Get unique order IDs from these items
    order_ids = list(set(item.order_id for item in seller_order_items))

    # Fetch these orders
    orders = Order.query.filter(Order.id.in_(order_ids)).all()

    orders_list = []
    for order in orders:
        # Filter order items to only include this seller's products
        seller_items_in_order = [item for item in order.items if item.product_id in seller_product_ids]
        items_list = []
        for item in seller_items_in_order:
             product = Product.query.get(item.product_id)
             items_list.append({
                "product_id": item.product_id,
                "product_name": product.name if product else 'Unknown Product',
                "quantity": item.quantity,
                "price_at_purchase": item.price_at_purchase
            })

        orders_list.append({
            "id": order.id,
            "buyer_user_id": order.user_id,
            "buyer_email": order.buyer.email if order.buyer else 'Unknown Buyer',
            "status": order.status,
            "tracking_number": order.tracking_number,
            "created_at": order.created_at.isoformat(),
            "seller_items_in_order": items_list # Only items from this seller
        })
    return jsonify(orders_list), 200

@app.route('/seller/payout/request', methods=['POST'])
@seller_required
def request_payout():
     if not g.current_user.seller_profile or not g.current_user.seller_profile.is_approved:
         return jsonify({"message": "User is not an approved seller"}), 403

     # Placeholder: Simulate payout request
     # In a real app, this would involve calculating earnings, interacting with a payout service (like Stripe Connect), etc.
     return jsonify({"message": "Payout request submitted (simulated)"}), 200

@app.route('/admin/users', methods=['GET'])
@admin_required
def admin_list_users():
    users = User.query.all()
    users_list = []
    for user in users:
         seller_info = None
         if user.role == 'seller' and user.seller_profile:
             seller_info = {
                "id": user.seller_profile.id,
                "shop_name": user.seller_profile.shop_name,
                "is_approved": user.seller_profile.is_approved
            }
         users_list.append({
             "id": user.id,
             "email": user.email,
             "role": user.role,
             "seller_profile": seller_info
         })
    return jsonify(users_list), 200

@app.route('/admin/sellers', methods=['GET'])
@admin_required
def admin_list_sellers():
    sellers = SellerProfile.query.all()
    sellers_list = []
    for seller in sellers:
        sellers_list.append({
            "id": seller.id,
            "user_id": seller.user_id,
            "user_email": seller.user.email if seller.user else 'Unknown User',
            "shop_name": seller.shop_name,
            "shop_description": seller.shop_description,
            "is_approved": seller.is_approved
        })
    return jsonify(sellers_list), 200

@app.route('/admin/sellers/<int:seller_id>/approve', methods=['PUT'])
@admin_required
def admin_approve_seller(seller_id):
    seller = SellerProfile.query.get(seller_id)
    if not seller:
        return jsonify({"message": "Seller profile not found"}), 404
    seller.is_approved = True
    # Ensure user role is 'seller' if not already
    if seller.user and seller.user.role != 'admin':
         seller.user.role = 'seller'
    db.session.commit()
    return jsonify({"message": "Seller approved", "seller_id": seller.id}), 200

@app.route('/admin/products', methods=['GET'])
@admin_required
def admin_list_products():
    products = Product.query.all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "stock": p.stock,
        "is_approved": p.is_approved,
        "seller_id": p.seller_id,
        "seller_shop_name": p.seller.shop_name if p.seller else None
    } for p in products]), 200

@app.route('/admin/products/<int:product_id>/approve', methods=['PUT'])
@admin_required
def admin_approve_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    product.is_approved = True
    db.session.commit()
    return jsonify({"message": "Product approved", "product_id": product.id}), 200

@app.route('/admin/orders', methods=['GET'])
@admin_required
def admin_list_orders():
    orders = Order.query.all()
    orders_list = []
    for order in orders:
        orders_list.append({
            "id": order.id,
            "user_id": order.user_id,
            "buyer_email": order.buyer.email if order.buyer else 'Unknown Buyer',
            "total_amount": order.total_amount,
            "status": order.status,
            "created_at": order.created_at.isoformat()
        })
    return jsonify(orders_list), 200

@app.route('/admin/reports/sales', methods=['GET'])
@admin_required
def admin_sales_report():
     # Basic sales report: total revenue from completed orders
     completed_orders = Order.query.filter_by(status='completed').all()
     total_revenue = sum(order.total_amount for order in completed_orders)
     return jsonify({"total_completed_sales_revenue": total_revenue}), 200

if __name__ == '__main__':
    # In a real deployment, you wouldn't use debug=True
    # and would configure host/port appropriately
    # For this demonstration, we run on http://127.0.0.1:5000/
    app.run(debug=True)