import os

# State Variables
orders = []  # List to store tuples/dicts: (order_id, product_name, quantity)
failed_entries = 0
total_tax = 0.0
transaction_history = []  # List to store every valid transaction amount entered


def load_inventory():
    """Reads saved inventory and transaction history from inventory.txt if it exists."""
    if not os.path.exists("inventory.txt"):
        return

    try:
        with open("inventory.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("Current Orders:") or line.startswith("Order successfully"):
                    continue

                parts = line.split(",")
                if len(parts) == 3:
                    order_id = int(parts[0].strip())
                    product_name = parts[1].strip()
                    quantity = int(parts[2].strip())
                    orders.append({"id": order_id, "product": product_name, "quantity": quantity})
                    transaction_history.append(quantity)
    except Exception as e:
        print(f"Error loading inventory file: {e}")


def save_inventory():
    """Saves the orders and transaction history to inventory.txt upon quit."""
    try:
        with open("inventory.txt", "w") as f:
            for order in orders:
                f.write(f"{order['id']}, {order['product']}, {order['quantity']}\n")
        print("\nOrder successfully saved to inventory.txt")
    except Exception as e:
        print(f"Error saving to file: {e}")


def get_valid_input():
    """Handles prompt for product name and quantity with input validation."""
    global failed_entries

    product_name = input("\nEnter Product Name: ").strip()
    if product_name.lower() == "quit":
        return "quit"

    if not product_name:
        print("Error: Product name cannot be empty.")
        failed_entries += 1
        return None

    qty_str = input("Enter Quantity: ").strip()
    if qty_str.lower() == "quit":
        return "quit"

    # Handle invalid input using isdigit()
    if not qty_str.isdigit():
        if qty_str.startswith("-") and qty_str[1:].isdigit():
            # Enforce business rules: Reject negative numbers
            print("Error: Negative numbers are not allowed.")
        else:
            print("Error: Quantity must be a valid non-negative integer.")

        failed_entries += 1
        return None

    return product_name, int(qty_str)


def process_delivery(current_total, new_value):
    """Calculates running total."""
    return current_total + new_value


def calculate_tax(amount):
    """Calculates 10% tax for a delivery amount."""
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    """Prints the final summary report."""
    print("\n=== Final Summary Report ===")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Tax Collected (10%): ${total_tax:.2f}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print(f"Transaction History: {transaction_history}")


# --- Execution Start ---

# 1. Persistence: Read existing inventory file at start
load_inventory()

# Display current stored orders initially
print("Current Orders:\n")
if orders:
    for order in orders:
        print(f"{order['id']}, {order['product']}, {order['quantity']}")
else:
    print("No existing orders found.")

# Main Loop
while True:
    result = get_valid_input()

    if result == "quit":
        # 3. Write-Back: Save on quit
        save_inventory()
        break

    if result is None:
        continue

    product_name, quantity = result

    # Assign next ID (starting at 1001)
    next_id = 1001 if not orders else orders[-1]["id"] + 1

    # 2. History Tracking: Store every valid transaction amount entered
    new_order = {"id": next_id, "product": product_name, "quantity": quantity}
    orders.append(new_order)
    transaction_history.append(quantity)

    # Calculate tax for this specific delivery
    tax_for_delivery = calculate_tax(quantity)
    total_tax += tax_for_delivery

    # Display new order output format
    print("\nNew Order Added:")
    print(f"{new_order['id']},{new_order['product']},{new_order['quantity']}")

    # Overstock Alert Check
    total_units = sum(order["quantity"] for order in orders)
    if total_units > 500:
        print("\nALERT: Overstock limit exceeded! Combined inventory exceeds 500 units.")
        save_inventory()
        break

# Final Reporting
total_units = sum(order["quantity"] for order in orders)
generate_report(total_units, failed_entries)