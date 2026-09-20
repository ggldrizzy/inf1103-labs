# Variables
inventory = {"Apple": 0, "Banana": 0, "Orange": 0}
failed_entries = 0
total_tax = 0.0

def get_valid_input():
    global failed_entries

    user_input = input(
        "\nEnter stock entry (e.g., 'Apple 15') or 'quit' to exit: "
    ).strip()

    if user_input.lower() == "quit":
        return "quit"

    # Split entry into stock type and quantity
    fruits = user_input.split()
    if len(fruits) != 2:
        print("Error: Format must be '<StockType> <Quantity>' (e.g., 'Banana 20').")
        failed_entries += 1
        return None

    stock_type, qty_str = fruits[0].capitalize(), fruits[1]

    # Validate stock type
    if stock_type not in inventory:
        print(
            f"Error: Unknown stock type '{stock_type}'. Choose Apple, Banana, or Orange."
        )
        failed_entries += 1
        return None

    # Handle invalid input using isdigit()
    if not qty_str.isdigit():
        if qty_str.startswith("-") and qty_str[1:].isdigit():
            # Enforce business rules: Reject negative numbers
            print("Error: Negative numbers are not allowed.")
        else:
            print("Error: Quantity must be a valid non-negative integer.")
        failed_entries += 1
        return None
    # Accept stock values as integers
    return stock_type, int(qty_str)

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

def generate_report(total_units, failed_attempts):
    print("\n=== Final Summary Report ===")
    print("Individual Stock Breakdown:")
    for item, count in inventory.items():
        print(f"  • {item}: {count} units")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Tax Collected (10%): ${total_tax:.2f}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

# Loop
print("Available Stock Types: Apple, Banana, Orange")

while True:
    result = get_valid_input()

    if result == "quit":
        break

    if result is None:
        continue

    stock_type, quantity = result

    # Calculate tax for this specific delivery
    tax_for_delivery = calculate_tax(quantity)
    total_tax += tax_for_delivery

    # Manage State: Update item total and calculate running total
    inventory[stock_type] = process_delivery(inventory[stock_type], quantity)
    total_units = sum(inventory.values())

    # Print current amount for each stock type after each valid entry
    print("\n--- Current Inventory Status ---")
    for item, count in inventory.items():
        print(f"{item}: {count} units")
    print(f"Total Combined Stock: {total_units}")
    print(f"Tax for this entry: ${tax_for_delivery:.2f}")
    print("-------------------------------")

    # Trigger Overstock Alert
    if total_units > 500:
        print("ALERT: Overstock limit exceeded! Combined inventory exceeds 500 units.")
        break

# Reporting
generate_report(sum(inventory.values()), failed_entries)