```
==============================================
Test Plan: E-commerce Website for Handmade Crafts
Version: 1.0
Date: 2023-10-27
Prepared By: QA Engineer
==============================================

1. Introduction

1.1. Purpose
The purpose of this document is to outline the test plan for the E-commerce Website for Handmade Crafts (V1). It describes the scope, approach, resources, and schedule of the testing activities. This plan ensures that the system meets the specified requirements and quality standards before release.

1.2. Product Overview
The E-commerce Website for Handmade Crafts is an online marketplace connecting artisans and customers. It facilitates product browsing, searching, purchasing, and provides tools for sellers to manage their shops and orders, and administrators to oversee the platform.

1.3. Goals of Testing
- Verify that all in-scope functional requirements are met.
- Ensure the system is user-friendly and meets usability requirements.
- Validate that security measures are adequate for user data and transactions.
- Assess system performance under expected load.
- Confirm responsiveness across different devices and browsers.
- Identify and report defects to be fixed before release.

1.4. Target Audience
This test plan is intended for the development team, project managers, business analysts, and other stakeholders involved in the project.

1.5. Glossary
- **API:** Application Programming Interface
- **CRUD:** Create, Read, Update, Delete
- **E2E:** End-to-End
- **FE:** Frontend
- **BE:** Backend
- **NFR:** Non-Functional Requirement
- **SPD:** Product Specification Document
- **UI:** User Interface
- **UX:** User Experience
- **JWT:** JSON Web Token
- **WCAG:** Web Content Accessibility Guidelines

2. Test Strategy

2.1. Types of Testing
The following types of testing will be performed:
- **Unit Testing:** Performed by developers to test individual functions or components in isolation (Frontend components, Backend functions/services).
- **Integration Testing:** Testing the interaction between integrated units or components (e.g., Frontend component interacting with API endpoint, Backend service interaction with database).
- **End-to-End (E2E) Testing:** Testing the complete user workflows from start to finish across the integrated system (e.g., Customer registration -> Product search -> Add to cart -> Checkout -> View order).
- **Functional Testing:** Verifying that each function of the software application performs as specified in the SPD. This will be the primary focus of documented test cases.
- **Non-Functional Testing:**
    - **Performance Testing:** Basic assessment of page load times and API response times against NFRs (Section 5, SPD).
    - **Security Testing:** Testing for common web vulnerabilities (OWASP Top 10 - basic checks), role-based access control validation.
    - **Usability Testing:** Evaluating the user-friendliness and intuitiveness of the interface and workflows.
    - **Responsiveness Testing:** Checking layout and functionality across different screen sizes (desktop, tablet, mobile) and orientations.
    - **Accessibility Testing:** Checking compliance with WCAG 2.1 Level AA guidelines (manual checks, automated tools like Lighthouse/Axe).

2.2. Test Levels
Testing will be conducted at the following levels:
- **Component Testing:** (Primarily Unit Testing by Developers)
- **Integration Testing:** Focusing on API endpoint testing and FE-BE communication.
- **System Testing:** Comprehensive testing of the integrated system (covering functional and non-functional types listed above).
- **User Acceptance Testing (UAT):** Final testing phase conducted by actual users or stakeholders to verify the system meets business needs.

2.3. Test Environments
Testing will be performed in environments that simulate production as closely as possible.
- **Development Environment:** Used for developer unit and initial integration testing.
- **Staging Environment:** A replica of the production environment used for system testing and UAT.

2.4. Test Data Management
- Test data will be created to cover various scenarios (e.g., different user roles, products with/without stock, orders with different statuses, users with/without reviews).
- Data creation scripts or tools may be used to populate the database.
- Care will be taken to handle sensitive data appropriately in non-production environments.

2.5. Test Tools
- **Test Management Tool:** (e.g., Jira, TestRail) for managing test cases, execution, and defect tracking.
- **Browser Developer Tools:** For inspecting elements, network requests, and responsiveness.
- **API Testing Tools:** (e.g., Postman, Insomnia) for manual API testing.
- **Automated Accessibility Tools:** (e.g., Lighthouse, Axe) for initial accessibility checks.
- **Automated Testing Frameworks:** (Future Consideration) For E2E (e.g., Cypress, Selenium) or API (e.g., Jest/Supertest). V1 will primarily focus on manual testing for comprehensive coverage, with automation planned for future iterations for regression.

2.6. Release Criteria
The system will be considered ready for release when the following criteria are met:
- All P0 (Blocker) and P1 (Critical) defects are resolved and verified.
- An agreed-upon percentage of P2 (Major) defects are resolved (e.g., >90%).
- All P3 (Minor) and P4 (Trivial) defects are reviewed and accepted by stakeholders, or scheduled for future sprints.
- All defined critical test cases (High/Medium Priority) are executed with a pass rate above a defined threshold (e.g., >95%).
- Key user workflows (Happy Paths) pass E2E testing.
- Non-functional requirements (basic performance, security, responsiveness, accessibility) are evaluated and meet acceptable levels.
- UAT is successfully completed.

3. Scope of Testing

Based on the SPD (Section 1.4, 2), the following features are in scope for testing in V1:

3.1. User Authentication & Authorization
- Customer, Seller, Admin registration and login.
- Role-based access control verification (e.g., non-sellers cannot create products, non-admins cannot access admin panel).
- Logout functionality.

3.2. Product Listing & Management (Seller Focus)
- Seller creating new product listings (including images, description, price, stock, category).
- Seller editing existing product details and stock.
- Seller deleting products.
- Product status/moderation flow (Admin approval - check if products become active).

3.3. Product Browsing, Search & Filtering (Customer Focus)
- Viewing products on the homepage (e.g., featured).
- Browsing all products on the Product Listing Page.
- Searching products by keywords.
- Filtering products by category, price range.
- Sorting products (e.g., by price, date).
- Viewing individual Product Details Page (images, description, price, seller info, reviews).

3.4. Shopping Cart Functionality (Customer Focus)
- Adding products to the cart from Product List/Detail pages.
- Viewing items in the shopping cart.
- Updating item quantities in the cart.
- Removing items from the cart.
- Cart persistence (basic check if items remain after navigation).

3.5. Checkout Process (Customer Focus)
- Proceeding from cart to checkout.
- Filling in shipping address details (validation).
- Payment integration interaction (simulated or actual gateway sandbox).
- Placing an order.
- Order confirmation (page/message).

3.6. Order Management
- **Customer:** Viewing their order history and individual order details/status.
- **Seller:** Viewing incoming orders for their products, viewing individual order details, updating order status (e.g., Shipped), adding tracking information.

3.7. User Profiles and Dashboards
- **Customer Dashboard:** Accessing order history, profile edit section.
- **Seller Dashboard:** Accessing product management, order management, shop setup (basic fields).
- Profile editing (name, potentially other non-sensitive details).

3.8. Product Reviews and Ratings (Customer Focus)
- Writing a review and providing a rating for a purchased product.
- Viewing reviews on the Product Detail Page.
- (Admin moderation of reviews is out of scope for V1 review creation, but viewing all reviews by admin is in scope).

3.9. Email Notifications (Basic Check)
- Order confirmation email (to customer).
- New order notification email (to seller).
- (Actual email content/delivery thoroughness depends on setup, focus on triggering).

3.10. Basic Admin Panel
- Admin Login.
- Viewing list of users (Customer, Seller, Admin).
- Viewing list of products (including moderation status).
- Moderating/Approving/Rejecting products.
- Viewing list of all orders.
- (Managing Categories, deleting users/products/orders directly by Admin - although DELETE endpoints exist, the UI for this might be limited in V1).

3.11. Responsive Web Design
- Checking layout and key functionality on different screen sizes (using browser developer tools responsive mode).

4. Out of Scope

Based on the SPD (Section 1.4, V1 Scope), the following features are out of scope for testing in this phase:
- Native Mobile Applications (iOS/Android)
- Advanced Seller Analytics & Reporting
- Community Forums or Social Networking Features
- Seller Marketing Tools (e.g., coupons, promotions)
- Complex Shipping Calculations (e.g., multi-origin shipping)
- Advanced Return/Refund Management workflows
- Admin panel Category Management UI.
- Admin deleting users, products, or orders via UI (backend endpoints might exist but UI testing is out).
- Testing different payment methods extensively (focus on one integrated method).
- Thorough email content/spam testing (focus on triggering).
- Security penetration testing (planned separately).
- Load testing beyond basic performance observations.

5. Test Deliverables

- Test Plan (this document)
- Test Cases (detailed below)
- Test Execution Report
- Defect Log / Bug Reports

6. Testing Schedule & Resources

(Note: Specific dates and resource allocation are not provided in the context. This section would be populated based on project timelines and available resources.)

- **Estimated Testing Start Date:** (To be determined)
- **Estimated Testing End Date:** (To be determined)
- **Resources:**
    - QA Team Members: (Number and names)
    - Test Environments: (Details)
    - Test Data: (Availability)

7. Risks & Contingencies

- **Risk:** Issues with Payment Gateway integration.
- **Mitigation:** Use gateway sandbox environment for testing. Have clear error handling and user communication for payment failures.
- **Risk:** Data inconsistencies between frontend and backend.
- **Mitigation:** Thorough integration and E2E testing, careful data validation on both ends.
- **Risk:** Performance degradation under moderate traffic.
- **Mitigation:** Conduct basic performance checks, identify potential bottlenecks early.
- **Risk:** Cross-browser/device compatibility issues.
- **Mitigation:** Test on a matrix of target browsers and devices/simulators, focusing on key flows.
- **Risk:** Delays in development impacting the testing schedule.
- **Contingency:** Prioritize test cases, focus on critical paths, communicate frequently with the development team.

8. Exit Criteria

As defined in Section 2.6.

9. Test Cases

The following section provides detailed test cases for key functionalities.

**Test Case Table Format:**

| Test Case ID | Description                                   | Preconditions                                                                 | Test Steps                                                                                                                               | Expected Result                                                                                                                               | Priority | Status |
| :----------- | :-------------------------------------------- | :---------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :----- |
|              |                                               |                                                                               |                                                                                                                                          |                                                                                                                                               |          |        |

---

**Test Cases: Customer Features**

| Test Case ID | Description                                   | Preconditions                                                                 | Test Steps                                                                                                                               | Expected Result                                                                                                                                               | Priority | Status |
| :----------- | :-------------------------------------------- | :---------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :----- |
| CUST_REG_01  | Successful Customer Registration              | - Not logged in.                                                              | 1. Navigate to the Registration page. <br> 2. Fill in valid Name, Email, Password. <br> 3. Select 'Customer' role. <br> 4. Submit the form. | User account is created with 'customer' role. User is logged in automatically or redirected to login. Success message displayed.             | High     | Open   |
| CUST_REG_02  | Registration with Existing Email              | - A user with the test email already exists.                                | 1. Navigate to Registration page. <br> 2. Enter details with an existing email. <br> 3. Submit the form.                                   | Registration fails. Error message "Email already exists" is displayed.                                                                        | High     | Open   |
| CUST_LOGIN_01| Successful Customer Login                     | - A customer account exists.                                                  | 1. Navigate to the Login page. <br> 2. Enter valid Customer Email and Password. <br> 3. Submit the form.                                | User is successfully logged in. Redirected to Customer Dashboard or Homepage. 'My Account' link is visible in header.                           | High     | Open   |
| CUST_LOGIN_02| Login with Invalid Credentials                | - Not logged in.                                                              | 1. Navigate to Login page. <br> 2. Enter incorrect Email or Password. <br> 3. Submit the form.                                            | Login fails. Error message "Invalid credentials" is displayed. User remains on Login page.                                                    | High     | Open   |
| CUST_PROD_01 | Browse Products (Product Listing Page)        | - Products exist in the database.                                             | 1. Navigate to the "Shop All" or Products page. <br> 2. Scroll through the list/grid.                                                   | Product listing page loads successfully. Products are displayed in a grid/list with basic info (image, name, price, seller). Pagination controls are visible if applicable. | High     | Open   |
| CUST_PROD_02 | Search Products (Valid Keyword)               | - Products exist, at least one matches keyword.                               | 1. Go to Homepage or Products page. <br> 2. Enter a valid keyword (e.g., "mug") in the search bar. <br> 3. Submit search.            | Product listing page loads showing only products matching the keyword. Relevant products appear.                                                | High     | Open   |
| CUST_PROD_03 | Search Products (No Match)                    | - Products exist, no product matches keyword.                                 | 1. Go to Homepage or Products page. <br> 2. Enter a non-matching keyword (e.g., "xyz123") in the search bar. <br> 3. Submit search.    | Product listing page loads showing no products. A "No products found" message is displayed.                                                     | High     | Open   |
| CUST_PROD_04 | Filter Products by Category                   | - Products with different categories exist. Categories endpoint is functional. | 1. Go to Products page. <br> 2. Select a specific category from the filter options. <br> 3. Apply filter.                             | Product list is updated to show only products belonging to the selected category.                                                              | High     | Open   |
| CUST_PROD_05 | Sort Products by Price (Ascending)            | - Multiple products with different prices exist.                                | 1. Go to Products page. <br> 2. Select 'Price: Low to High' from the sort options.                                                       | Product list is reordered with the lowest priced items appearing first.                                                                        | Medium   | Open   |
| CUST_PROD_06 | View Product Detail Page                      | - A product exists and is active/approved.                                    | 1. Go to Products page. <br> 2. Click on a specific product card.                                                                        | Product Detail Page loads for the selected product. All details (images, description, price, stock, seller info, reviews) are displayed correctly. | High     | Open   |
| CUST_CART_01 | Add Product to Empty Cart                     | - A product is active/approved and in stock.                                  | 1. Go to Product Detail Page for a product. <br> 2. Click "Add to Cart". <br> 3. Click Cart icon or navigate to Cart page.             | Product is successfully added to the cart. Cart icon shows item count (1). Cart page shows the product with quantity 1 and correct subtotal.      | High     | Open   |
| CUST_CART_02 | Add Same Product Multiple Times               | - A product is active/approved and in stock > 1.                              | 1. Add a product to cart (Qty 1). <br> 2. Go back to the product page or click "Add to Cart" again. <br> 3. View Cart.             | The quantity of the existing item in the cart is increased (e.g., to 2). The item subtotal and cart total are updated accordingly.               | High     | Open   |
| CUST_CART_03 | Add Different Product                         | - Multiple products are active/approved and in stock.                         | 1. Add Product A to cart. <br> 2. Add Product B to cart. <br> 3. View Cart.                                                               | Both Product A and Product B are listed as separate items in the cart with correct quantities (default 1 if not specified) and subtotals. Cart total is sum of item subtotals. | High     | Open   |
| CUST_CART_04 | Update Item Quantity in Cart                  | - An item is in the cart. Product stock allows increase.                      | 1. Go to Cart page. <br> 2. Change the quantity of an item using the input field (e.g., from 1 to 3).                                | The item quantity is updated. The item subtotal and the overall cart total are recalculated and displayed correctly.                            | High     | Open   |
| CUST_CART_05 | Update Item Quantity Beyond Stock             | - An item is in the cart. Product has limited stock.                          | 1. Go to Cart page. <br> 2. Try to change item quantity to be greater than available stock.                                           | The quantity input should prevent entering a value higher than stock, or an error/warning message should appear upon attempting the update.     | Medium   | Open   |
| CUST_CART_06 | Remove Item from Cart                         | - Multiple items are in the cart.                                           | 1. Go to Cart page. <br> 2. Click the "Remove" button for one item.                                                                     | The selected item is removed from the cart. The cart total is updated. The remaining item(s) are still listed.                                  | High     | Open   |
| CUST_CART_07 | Remove Last Item from Cart                    | - Only one item is in the cart.                                             | 1. Go to Cart page. <br> 2. Click the "Remove" button for the last item.                                                                 | The item is removed. The cart becomes empty. An "Your cart is empty" message and a link to continue shopping should be displayed.               | High     | Open   |
| CUST_CHECK_01| Successful Checkout (Happy Path)              | - User is logged in as Customer. <br> - Cart has items. <br> - Payment gateway simulation is set up. | 1. Go to Cart page. <br> 2. Click "Proceed to Checkout". <br> 3. Fill in valid Shipping Address details. <br> 4. Enter simulated payment details via gateway elements. <br> 5. Click "Place Order". | User is redirected to Order Confirmation page or sees a success message. Cart is cleared. Order is created in backend with 'Pending' status. Email notification triggered. | High     | Open   |
| CUST_CHECK_02| Checkout with Empty Cart                      | - User is logged in as Customer. <br> - Cart is empty.                        | 1. Try to navigate to the Checkout page directly OR clear cart on cart page and click checkout.                                      | User should be prevented from accessing the checkout page and redirected back to the Cart or Shopping page with a message.                      | High     | Open   |
| CUST_CHECK_03| Checkout - Shipping Address Validation        | - User is logged in. <br> - Cart has items.                                   | 1. Go to Checkout. <br> 2. Leave required shipping address fields empty or invalid. <br> 3. Try to submit the form.                     | Client-side validation prevents submission, highlighting required/invalid fields. Error messages are displayed next to fields.                    | High     | Open   |
| CUST_ORDER_01| View Customer Order History                   | - User is logged in as Customer. <br> - Customer has placed orders.           | 1. Go to Customer Dashboard. <br> 2. Click "Order History".                                                                            | A list of the customer's past orders is displayed, showing basic info (Order ID, Date, Status, Total). Orders are sorted latest first.         | High     | Open   |
| CUST_ORDER_02| View Specific Customer Order Details          | - User is logged in as Customer. <br> - Customer has placed orders.           | 1. Go to Order History. <br> 2. Click on a specific Order ID/link in the list.                                                       | Order Detail page loads for that order. Full details (items purchased, quantities, prices, shipping address, current status, tracking number) are displayed. | High     | Open   |
| CUST_REVIEW_01| Write Review (Eligible Purchase)              | - User is logged in as Customer. <br> - User has purchased the product.     | 1. Go to the Product Detail Page of a purchased item. <br> 2. Find the "Write a Review" section. <br> 3. Select a rating (1-5 stars). <br> 4. Enter an optional comment. <br> 5. Submit the review. | Review is successfully submitted and appears in the reviews list for that product (after potential moderation/delay). Success message displayed. Product's average rating and review count may update. | High     | Open   |
| CUST_PROFILE_01| View Customer Profile Settings               | - User is logged in as Customer.                                              | 1. Go to Customer Dashboard. <br> 2. Click "Profile Settings".                                                                           | Profile page loads showing editable fields (e.g., Name, Email - non-editable). Current information is pre-filled.                             | Medium   | Open   |
| CUST_PROFILE_02| Update Customer Profile Settings              | - User is logged in as Customer.                                              | 1. Go to Profile Settings. <br> 2. Modify one or more allowed fields (e.g., Name). <br> 3. Save changes.                                | Profile information is updated successfully in the backend. Updated information is displayed after saving. Success message displayed.           | Medium   | Open   |

---

**Test Cases: Seller Features**

| Test Case ID | Description                                   | Preconditions                                                                 | Test Steps                                                                                                                               | Expected Result                                                                                                                                               | Priority | Status |
| :----------- | :-------------------------------------------- | :---------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :----- |
| SELL_REG_01  | Successful Seller Registration                | - Not logged in.                                                              | 1. Navigate to Registration page. <br> 2. Fill in valid Name, Email, Password, Shop Name. <br> 3. Select 'Seller' role. <br> 4. Submit form. | User account created with 'seller' role. Seller profile is created and linked. User is logged in or redirected. Success message. Shop Name is saved.          | High     | Open   |
| SELL_LOGIN_01| Successful Seller Login                       | - A seller account exists.                                                    | 1. Navigate to Login page. <br> 2. Enter valid Seller Email and Password. <br> 3. Submit form.                                            | User is successfully logged in with 'seller' role. Redirected to Seller Dashboard or Homepage. 'My Account' link in header leads to Seller Dashboard.     | High     | Open   |
| SELL_PROD_01 | Create New Product Listing (Seller)           | - User is logged in as Seller. <br> - Categories exist.                       | 1. Go to Seller Dashboard. <br> 2. Navigate to Product Management. <br> 3. Click "Add New Product". <br> 4. Fill in all required product details (Name, Price, Stock, Category) and optional fields (Description). <br> 5. Upload image(s). <br> 6. Submit form. | Product listing is created in the backend, linked to the seller. Initial status is 'Pending' for admin moderation. Seller sees the product in their list. Images are uploaded/linked. | High     | Open   |
| SELL_PROD_02 | Edit Existing Product Listing (Seller)        | - User is logged in as Seller. <br> - Seller has existing products.           | 1. Go to Seller Dashboard -> Product Management. <br> 2. Select an existing product. <br> 3. Modify details (e.g., Price, Stock, Description). <br> 4. (Optional) Add/Remove/Replace images. <br> 5. Save changes. | Product details are updated in the backend. Changes are reflected in the seller's product list. Images are handled correctly.                               | High     | Open   |
| SELL_PROD_03 | Delete Product Listing (Seller)               | - User is logged in as Seller. <br> - Seller has existing products.           | 1. Go to Seller Dashboard -> Product Management. <br> 2. Select a product. <br> 3. Click "Delete Product". <br> 4. Confirm deletion.    | Product is removed from the seller's list and no longer visible on the public site. Associated data (images) are handled appropriately (deleted or marked). | Medium   | Open   |
| SELL_ORDER_01| View Seller Orders Dashboard                  | - User is logged in as Seller. <br> - Orders for seller's products exist.     | 1. Go to Seller Dashboard. <br> 2. Navigate to Order Management.                                                                         | A list of orders containing products from this seller is displayed. List includes order ID, date, customer info (basic), and status.                  | High     | Open   |
| SELL_ORDER_02| View Specific Seller Order Details            | - User is logged in as Seller. <br> - Orders for seller's products exist.     | 1. Go to Seller Order Management. <br> 2. Click on a specific Order ID/link.                                                           | Order Detail page loads, showing details relevant to the seller (customer shipping address, items from THIS seller's shop in that order, status).       | High     | Open   |
| SELL_ORDER_03| Update Order Status (Seller)                  | - User is logged in as Seller. <br> - An order for seller's product is 'Processing'. | 1. Go to Order Details for an eligible order. <br> 2. Find the status update option. <br> 3. Change status to 'Shipped'. <br> 4. Enter tracking number. <br> 5. Save changes. | Order status is updated to 'Shipped' in the backend. Tracking number is saved. Status change is reflected in the seller's order view. Email notification triggered. | High     | Open   |

---

**Test Cases: Admin Features**

| Test Case ID | Description                                   | Preconditions                                                                 | Test Steps                                                                                                                               | Expected Result                                                                                                                                               | Priority | Status |
| :----------- | :-------------------------------------------- | :---------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :----- |
| ADMIN_LOGIN_01| Successful Admin Login                        | - An admin account exists.                                                    | 1. Navigate to Login page. <br> 2. Enter valid Admin Email and Password. <br> 3. Submit form.                                            | User is successfully logged in with 'admin' role. Redirected to Admin Dashboard or Homepage. Access to Admin panel links is available.                    | Critical | Open   |
| ADMIN_AUTH_01| Access Admin Route (Unauthorized User)        | - User is logged in as Customer or Seller, OR not logged in.                  | 1. Try to directly access an Admin URL (e.g., /api/v1/admin/users or /dashboard/admin).                                                | Access is denied. User receives a 403 Forbidden or 401 Unauthorized error response (API). Frontend should handle this gracefully (e.g., redirect to login/403 page). | Critical | Open   |
| ADMIN_USERS_01| View All Users (Admin)                        | - User is logged in as Admin. <br> - Multiple users (Cust, Sell, Admin) exist. | 1. Go to Admin Dashboard. <br> 2. Navigate to User Management section (or equivalent link).                                             | A list of all users (Customer, Seller, Admin) is displayed, including their basic details (ID, Name, Email, Role).                                     | High     | Open   |
| ADMIN_PROD_01| View All Products for Moderation (Admin)      | - User is logged in as Admin. <br> - Products with different statuses exist.    | 1. Go to Admin Dashboard. <br> 2. Navigate to Product Moderation section (or equivalent link).                                         | A list of all products is displayed, including their key details (Name, Seller, Category, Price, Stock, Moderation Status, isActive). Filtering/sorting options might be available. | High     | Open   |
| ADMIN_PROD_02| Moderate Product - Approve (Admin)            | - User is logged in as Admin. <br> - A product is in 'Pending' status.        | 1. Go to Product Moderation list. <br> 2. Select a 'Pending' product. <br> 3. Change its status to 'Approved' and set isActive to true. <br> 4. Save changes. | Product status is updated to 'Approved' and isActive to true in the backend. The product becomes visible on the public site. Change is reflected in the admin list. | High     | Open   |
| ADMIN_PROD_03| Moderate Product - Reject (Admin)             | - User is logged in as Admin. <br> - A product is in 'Pending' status.        | 1. Go to Product Moderation list. <br> 2. Select a 'Pending' product. <br> 3. Change its status to 'Rejected' and set isActive to false. <br> 4. Save changes. | Product status is updated to 'Rejected' and isActive to false. The product does not become visible on the public site (or is removed if it was public). Change reflected in admin list. | High     | Open   |
| ADMIN_ORDERS_01| View All Orders (Admin)                       | - User is logged in as Admin. <br> - Multiple orders exist.                   | 1. Go to Admin Dashboard. <br> 2. Navigate to Order Overview section (or equivalent link).                                             | A list of all orders is displayed, including Order ID, Customer, Seller(s) involved (implied via items), Status, Total Amount, Date. Filtering/sorting options might be available. | High     | Open   |
| ADMIN_ORDERS_02| View Specific Order Details (Admin)           | - User is logged in as Admin. <br> - Orders exist.                            | 1. Go to All Orders list. <br> 2. Click on a specific Order ID/link.                                                                     | Full Order Details page loads, showing all information about the order (Customer info, Shipping Address, all Order Items with associated Product/Seller info, Status, Payment Status, Tracking). | High     | Open   |
| ADMIN_ORDERS_03| Update Order Status (Admin)                   | - User is logged in as Admin. <br> - An order exists.                         | 1. Go to Order Details for an order. <br> 2. Find the status update option. <br> 3. Change status (e.g., from 'Shipped' to 'Delivered'). <br> 4. Save changes. | Order status is updated in the backend. Change is reflected in the admin order view (and potentially customer/seller views).                             | Medium   | Open   |

---

**Test Cases: Non-Functional (Examples)**

| Test Case ID   | Description                                     | Preconditions                                   | Test Steps                                                                                                | Expected Result                                                                                                | Priority | Status |
| :------------- | :---------------------------------------------- | :---------------------------------------------- | :-------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------- | :------- | :----- |
| NFR_RESP_01    | Homepage Responsiveness (Mobile)                | - Use a mobile device or browser emulator.      | 1. Navigate to the Homepage. <br> 2. Observe layout and navigation. <br> 3. Interact with elements.      | Layout adjusts correctly for smaller screen. Navigation is usable (e.g., hamburger menu). Elements are clickable. | High     | Open   |
| NFR_RESP_02    | Product Detail Page Responsiveness (Tablet)     | - Use a tablet device or browser emulator.      | 1. Navigate to a Product Detail Page. <br> 2. Observe layout of images, details, and sections.            | Layout adjusts correctly for tablet screen. Content sections are readable and well-organized.                      | High     | Open   |
| NFR_PERF_01    | Homepage Load Time (Basic Check)                | - Use browser developer tools (Network tab).    | 1. Clear browser cache and cookies. <br> 2. Navigate to the Homepage. <br> 3. Observe page load time.    | Homepage loads within acceptable time (e.g., < 3 seconds as per NFR, Section 5).                               | Medium   | Open   |
| NFR_PERF_02    | Product Listing Load Time (Basic Check)         | - Use browser developer tools (Network tab).    | 1. Clear browser cache and cookies. <br> 2. Navigate to the Product Listing Page. <br> 3. Observe load time. | Product Listing page loads within acceptable time (e.g., < 3 seconds as per NFR, Section 5).                   | Medium   | Open   |
| NFR_SEC_01     | Role-Based Access (API Level)                   | - Logged in with different roles. <br> - Use API testing tool. | 1. Log in as Customer, get JWT. <br> 2. Try to access Seller or Admin API endpoints using the customer JWT. <br> 3. Repeat for Seller trying Admin endpoints. | API returns 403 Forbidden for unauthorized access attempts.                                                  | Critical | Open   |
| NFR_SEC_02     | Protect Sensitive Endpoints                     | - Not logged in. <br> - Use API testing tool.   | 1. Try to access protected API endpoints (e.g., /api/v1/users/me, /api/v1/orders) without a token.       | API returns 401 Unauthorized for attempts to access protected resources without authentication.                  | Critical | Open   |
| NFR_USABILITY_01| Checkout Flow Intuition                       | - Not logged in or logged in. <br> - Cart has items. | 1. Start from adding an item to the cart. <br> 2. Proceed through the entire checkout process.           | The steps are logical and easy to follow. Required fields are clear. Feedback is provided (e.g., on errors).     | High     | Open   |
| NFR_ACC_01     | Basic Accessibility Check (Homepage)            | - Use browser accessibility tools (e.g., Axe).  | 1. Navigate to Homepage. <br> 2. Run automated accessibility checker. <br> 3. Perform basic keyboard navigation test. | Automated checker reports minimal critical/serious issues. User can navigate key interactive elements using keyboard. | Medium   | Open   |

---
```