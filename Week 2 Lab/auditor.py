

# Variables
inventory = {"Apple": 0, "Banana": 0, "Orange": 0}
failed_entries = 0

print("Available Stock Types: Apple, Banana, Orange")

# Loop
while True:
    user_input = input(
        "\nEnter stock entry (e.g., 'Apple 15') or 'quit' to exit: "
    ).strip()

    if user_input.lower() == "quit":
        break

    # Split entry into stock type and quantity
    fruits = user_input.split()
    if len(fruits) != 2:
        print("Error: Format must be '<StockType> <Quantity>' (e.g., 'Banana 20').")
        failed_entries += 1
        continue

    stock_type, qty_str = fruits[0].capitalize(), fruits[1]

    # Validate stock type
    if stock_type not in inventory:
        print(f"Error: Unknown stock type '{stock_type}'. Choose Apple, Banana, or Orange.")
        failed_entries += 1
        continue

    # Handle invalid input using isdigit()
    if not qty_str.isdigit():
        if qty_str.startswith("-") and qty_str[1:].isdigit():
            # Enforce business rules: Reject negative numbers
            print("Error: Negative numbers are not allowed.")
        else:
            print("Error: Quantity must be a valid non-negative integer.")

        failed_entries += 1
        continue

    # Accept stock values as integers
    quantity = int(qty_str)

    # Manage State: Update item total and calculate running total
    inventory[stock_type] += quantity
    total_units = sum(inventory.values())

    # PRINT CURRENT AMOUNT FOR EACH STOCK TYPE AFTER EACH VALID ENTRY
    print("\n--- Current Inventory Status ---")
    for item, count in inventory.items():
        print(f"{item}: {count} units")
    print(f"Total Combined Stock: {total_units}")
    print("-------------------------------")

    # Trigger Overstock Alert
    if total_units > 500:
        print("ALERT: Overstock limit exceeded! Combined inventory exceeds 500 units.")
        break

# Reporting
print("\n=== Final Summary Report ===")
print("Individual Stock Breakdown:")
for item, count in inventory.items():
    print(f"  • {item}: {count} units")
print(f"Total Units Processed: {sum(inventory.values())}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")