from http import client
import requests
import json
import string
import random

# Gateway URL
GATEWAY_URL = "http://localhost:8000"
PRODUCT_URL = "http://localhost:8002"

def test_system():
    print("Starting the end-to-end test...\n")


    # Step 1: Register a user
    print("Registering a user...")
    username = "testuser" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    register_data = {
        "username": username,
        "password": "securepassword",
        "email": f"{username}@example.com"
    }
    register_response = requests.post(f"{GATEWAY_URL}/register", json=register_data)
    print("Register response:", register_response.json())
    assert register_response.status_code == 200, "Failed to register user"
    username = register_data["username"]


    # Step 2: Login the user through the Gateway
    print("Logging in the user through the Gateway...")
    login_data = {
        "username": username,
        "password": "securepassword"
    }
    login_response = requests.post(f"{GATEWAY_URL}/login", data=login_data)
    assert login_response.status_code == 200, "Failed to login user"
    token = login_response.json().get("access_token")
    assert token, "No token received upon login"
    headers = {"Authorization": f"Bearer {token}"}
    print("Login token: ", token)

    # Step 2.5: Test validate-token route
    print("Validating token...")
    validate_response = requests.get(
        f"{GATEWAY_URL}/validate-token",
        params={"token": token}
    )
    print("Validate token response:", validate_response.json())
    assert validate_response.status_code == 200, "Failed to validate token"
    assert validate_response.json()["msg"] == "Token is valid."

    # Step 3: Add item to ongoing order
    print("Adding first item to order...")
    order_data = {
        "name": "Product 1",
        "quantity": 1
    }
    response = requests.post(f"{GATEWAY_URL}/orders/add_item/", json=order_data, headers=headers)
    print("add item request sent")
    assert response.status_code == 200, "Failed to add item to order"
    print(f"Item added to order successfully. Order ID: {response.json().get('order_id')}")

    print("Adding second item to order...")
    order_data = {
        "name": "Product 1",
        "quantity": 2
    }
    response2 = requests.post(f"{GATEWAY_URL}/orders/add_item/", json=order_data, headers=headers)
    assert response2.status_code == 200, "Failed to add item to order"
    print(f"Item added to order successfully. Order ID: {response2.json().get('order_id')}")

    print("Adding third item to order...")
    order_data = {
        "name": "Product 2",
        "quantity": 3
    }
    response3 = requests.post(f"{GATEWAY_URL}/orders/add_item/", json=order_data, headers=headers)
    assert response3.status_code == 200, "Failed to add item to order"
    print(f"Item added to order successfully. Order ID: {response3.json().get('order_id')}")
    
    # step3.5 get ongoing order
    response4 = requests.get(f"{GATEWAY_URL}/orders/ongoing/", headers=headers)
    assert response4.status_code == 200, "Failed to get ongoing order"
    print(f"Items inongoing order: {response4.json()}")

    # Step 4: Finalize the order
    print("Finalizing the order...")
    finalize_response = requests.post(f"{GATEWAY_URL}/orders/finalize", headers=headers)
    assert finalize_response.status_code == 200, "Failed to finalize order"
    print(f"Order finalized successfully: {finalize_response.json()}")

    # Step 5: Process payment for the order
    print("Processing payment for the first finalized order...")
    payment_data = {
        "cc_number": "1234-5678-9101-1121"  # Example credit card number
    }
    payment_response = requests.post(f"{GATEWAY_URL}/pay_order/", json=payment_data, headers=headers)
    assert payment_response.status_code == 200, "Payment failed"
    print(f"Payment successful for the finalized order.")

    # Step 6: Verify that the order status has been updated to 'paid'
    # After payment, the first finalized order's state should change to 'paid'
    print("Verifying order status after payment...")

    # Fetch all orders for the user from the Gateway
    order_status_response = requests.get(f"{GATEWAY_URL}/orders/", headers=headers)
    assert order_status_response.status_code == 200, "Failed to fetch order status"

    # Get the order details from the response
    orders = order_status_response.json().get("orders", [])
    assert orders, "No orders found"
    print(orders)

    # Find the order that was finalized and check its status
    finalized_order = next((order for order in orders if order["state"] == "paid"), None)
    assert finalized_order, "No finalized order found"
    assert finalized_order['state'] == "paid", "Order status is not updated to 'paid'"

    print(f"Order status verified as 'paid'.")


    # Step 5: Logout the user
    print("Logging out the user...")
    logout_response = requests.post(f"{GATEWAY_URL}/logout", headers=headers)
    assert logout_response.status_code == 200, "Failed to logout user"

    # Step 6: Verify token invalidation
    print("Verifying token invalidation...")
    protected_response = requests.get(f"{GATEWAY_URL}/products/", headers=headers)
    assert protected_response.status_code != 401, "Token should be invalidated after logout"
    print("Passed the test for invalidated token after logout")

    # Step 7: Admin user creates a product
    print("Admin creating a product...")
    admin_login_data = {
        "username": "admin",
        "password": "admin"
    }

    admin_product_response = requests.post(f"{PRODUCT_URL}/products/", json={
        "name": "Product"+ ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3)) ,
        "price": 50.0,
        "description": "description of Product",
        "available_item": 2
    })
    assert admin_product_response.status_code == 200, "Admin failed to create product"

 

    print("End-to-end test completed successfully.")

# Run the test
if __name__ == "__main__":
    test_system()
