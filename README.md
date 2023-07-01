# Little Lemon Restaurant API

## Introduction
The Little Lemon Restaurant API provides access to various functionalities for interacting with the restaurant's menu, placing orders, and managing user roles. This API allows clients to develop web and mobile applications to enhance the restaurant's services. Below are the available endpoints:

## Endpoints

### User Registration and Authentication

- POST /api/users: Register a new user account.
- GET /api/users/me: Retrieve details of the current user.
- POST /token/login: Generate access tokens for authentication.

### Menu Items

- GET /api/menu-items: Retrieve a list of all menu items.
- POST /api/menu-items: Create a new menu item.
- GET /api/menu-items/{menuItem}: Retrieve details of a specific menu item.
- PUT /api/menu-items/{menuItem}: Update a specific menu item.
- DELETE /api/menu-items/{menuItem}: Delete a specific menu item.

### User Group Management

- GET /api/groups/manager/users: Retrieve a list of all managers.
- POST /api/groups/manager/users: Assign a user to the manager group.
- DELETE /api/groups/manager/users/{userId}: Remove a user from the manager group.
- GET /api/groups/delivery-crew/users: Retrieve a list of all delivery crew members.
- POST /api/groups/delivery-crew/users: Assign a user to the delivery crew group.
- DELETE /api/groups/delivery-crew/users/{userId}: Remove a user from the delivery crew group.

### Cart Management

- GET /api/cart/menu-items: Retrieve the items in the user's cart.
- POST /api/cart/menu-items: Add a menu item to the user's cart.
- DELETE /api/cart/menu-items: Remove all items from the user's cart.

### Order Management

- GET /api/orders: Retrieve all orders placed by the user.
- POST /api/orders: Place a new order.
- GET /api/orders/{orderId}: Retrieve details of a specific order.
- PUT /api/orders/{orderId}: Update an order by assigning a delivery crew and updating the order status.
- DELETE /api/orders/{orderId}: Delete a specific order.
- PATCH /api/orders/{orderId}: Update the order status (0 or 1) as a delivery crew member.

## Getting Started

To use the Little Lemon Restaurant API, follow these steps:

1. Clone or fork the repository to your local machine.
2. Install the required dependencies using the `pipenv` command and the provided `Pipfile.lock` file:
   pipenv install
3.  run the applicaion 

## Conclusion
The Little Lemon Restaurant API provides convenient endpoints to manage user registration, authentication, menu items, carts, orders, and user group management. Refer to the API documentation for detailed information on request/response formats and required parameters.
