import json
import os

# Global inventory list
inventory = []

# --- Requirement 3: Data Persistence Functions ---

def load_inventory():
    global inventory
    filename = "inventory.json"
    
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                inventory = json.load(file)
            print("inventory.json found.")
            print("Inventory loaded successfully.")
        except json.JSONDecodeError:
            print("inventory.json is corrupted. Starting with an empty inventory.")
            inventory = []
    else:
        # Default initial data if inventory.json does not exist yet
        inventory = [
            {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
            {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
        ]

def save_inventory(show_message=True):
    filename = "inventory.json"
    if show_message:
        print("Saving inventory...")
    
    with open(filename, "w") as file:
        json.dump(inventory, file, indent=4)
        
    print("Inventory saved successfully to inventory.json." if show_message else "Inventory saved successfully.")

# --- Requirement 2: Data Manipulation Functions ---

def display_all():
    print("\nCurrent Inventory")
    print("-" * 45)
    if not inventory:
        print("Inventory is empty.")
    else:
        for item in inventory:
            print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print("-" * 45)

def add_product():
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))
    
    new_product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }
    inventory.append(new_product)
    print("\nProduct added successfully!")

def update_stock():
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    
    for item in inventory:
        if item["id"] == product_id:
            print(f"\nProduct Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['stock']}\n")
            
            new_stock = int(input("New Stock Quantity: "))
            item["stock"] = new_stock
            print("\nStock updated successfully!")
            return
            
    print("\nProduct not found.")

def search_product():
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    
    for item in inventory:
        if item["id"] == product_id:
            print("\nProduct Found")
            print("-" * 45)
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['stock']}")
            print("-" * 45)
            return
            
    print("\nProduct not found.")

# --- Requirement 4: Menu System ---

def main_menu():
    print("==============================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("==============================================\n")
    
    # Load inventory at startup
    load_inventory()
    
    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")
        
        choice = input("\nEnter option: ").strip()
        
        if choice == "1":
            display_all()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_stock()
        elif choice == "4":
            search_product()
        elif choice == "5":
            print()
            save_inventory(show_message=True)
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(show_message=False)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()