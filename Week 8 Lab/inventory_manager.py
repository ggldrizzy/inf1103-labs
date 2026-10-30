import json
import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(BASE_DIR, "inventory.json")

# --- 1. Product Class (Responsible for a single product's state & behavior) ---
class Product:
    def __init__(self, product_id, name, price, stock):
        self._product_id = product_id   
        self.name = name
        self._price = price             
        self._stock = stock             

    @property
    def product_id(self):
        return self._product_id

    @property
    def price(self):
        return self._price

    @property
    def stock(self):
        return self._stock

    def update_stock(self, quantity):
        """Encapsulates stock modification behavior inside the class."""
        self._stock = quantity

    def display_information(self):
        """Displays individual product information."""
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock}")

    def to_dict(self):
        """Helper to serialize product object into a dictionary for JSON storage."""
        return {
            "id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock
        }


# --- 2. Inventory Class (Responsible for managing a collection of products) ---
class Inventory:
    def __init__(self):
        self.products = []  # Collection of Product objects

    def add_product(self, product):
        self.products.append(product)

    def search_product(self, product_id):
        for item in self.products:
            if item.product_id == product_id:
                return item
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 45)
        if not self.products:
            print("Inventory is empty.")
        else:
            for item in self.products:
                item.display_information()
        print("-" * 45)


# --- 3. File Handling Functions ---
def load_inventory(inventory_obj):
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
                inventory_obj.products = []
                for item in data:
                    # Reconstruct Product objects from dictionary data
                    product = Product(item["id"], item["name"], item["price"], item["stock"])
                    inventory_obj.add_product(product)
            print("inventory.json found.")
            print("Inventory loaded successfully.")
        except json.JSONDecodeError:
            print("inventory.json is corrupted. Starting with an empty inventory.")
            inventory_obj.products = []
    else:
        inventory_obj.products = []

def save_inventory(inventory_obj, show_message=True):
    if show_message:
        print("Saving inventory...")
    
    # Convert Product objects back to dictionaries for JSON serialization
    data = [product.to_dict() for product in inventory_obj.products]
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)
        
    print("Inventory saved successfully to inventory.json." if show_message else "Inventory saved successfully.")


# --- 4. Main Menu & User Interaction ---
def main_menu():
    print("==============================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("==============================================\n")
    
    # Create Inventory object
    inventory = Inventory()
    
    # Load inventory at startup
    load_inventory(inventory)
    
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
            inventory.display_all()
        elif choice == "2":
            print("\nAdd New Product")
            product_id = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            price = float(input("Price: "))
            stock = int(input("Stock Quantity: "))
            
            new_product = Product(product_id, name, price, stock)
            inventory.add_product(new_product)
            print("\nProduct added successfully!")
        elif choice == "3":
            print("\nUpdate Stock")
            product_id = input("Enter Product ID: ").strip()
            
            product = inventory.search_product(product_id)
            if product:
                print(f"\nProduct Found:")
                print(f"Name: {product.name}")
                print(f"Current Stock: {product.stock}\n")
                
                new_stock = int(input("New Stock Quantity: "))
                product.update_stock(new_stock) # Controlled via encapsulation method
                print("\nStock updated successfully!")
            else:
                print("\nProduct not found.")
        elif choice == "4":
            print("\nSearch Product")
            product_id = input("Enter Product ID: ").strip()
            
            product = inventory.search_product(product_id)
            if product:
                print("\nProduct Found")
                print("-" * 45)
                product.display_information()
                print("-" * 45)
            else:
                print("\nProduct not found.")
        elif choice == "5":
            print()
            save_inventory(inventory, show_message=True)
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory, show_message=False)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()