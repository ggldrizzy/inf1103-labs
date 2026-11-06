import json
import os
from abc import ABC, abstractmethod

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(BASE_DIR, "inventory.json")


# Interface Definition (ABC)
class CanBeShipped(ABC):
    """Interface contract for items that require physical shipping."""

    @abstractmethod
    def calculate_shipping_cost(self):
        pass


# Abstract Base Class 
class Product(ABC):
    """Abstract Base Class for products. Cannot be instantiated directly."""

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
        """Displays base product information."""
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock}", end="")

    @abstractmethod
    def get_fulfilment_info(self):
        """Abstract method to be implemented by concrete product subclasses."""
        pass

    @abstractmethod
    def to_dict(self):
        """Abstract method for dictionary serialization for JSON storage."""
        pass


# Concrete Subclasses
class PhysicalProduct(Product, CanBeShipped):
    """Represents a physical product with weight and shipping capabilities."""

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.weight = float(weight)  # Weight in kilograms

    def display_information(self):
        # Reuse parent implementation and extend with subclass specific details
        super().display_information()
        print(f" | Weight: {self.weight}kg | Shipping: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self):
        return f"Product requires physical shipping. Weight: {self.weight}kg."

    def calculate_shipping_cost(self):
        # Simple rule: $5.00 base fee + $2.00 per kg
        return 5.00 + (self.weight * 2.00)

    def to_dict(self):
        return {
            "type": "physical",
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "weight": self.weight
        }


class DigitalProduct(Product):
    """Represents a digital product delivered via digital download."""

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.download_size = float(download_size)  # Size in megabytes

    def display_information(self):
        # Reuse parent implementation and extend with subclass specific details
        super().display_information()
        print(f" | Download Size: {self.download_size}MB")

    def get_fulfilment_info(self):
        return f"Product is delivered digitally. Download size: {self.download_size}MB."

    def to_dict(self):
        return {
            "type": "digital",
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "download_size": self.download_size
        }


# Inventory Class
class Inventory:
    """Manages a collection of Product instances."""

    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def search_product(self, product_id):
        for item in self.products:
            if item.product_id == product_id:
                return item
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 65)
        if not self.products:
            print("Inventory is empty.")
        else:
            for item in self.products:
                item.display_information()
        print("-" * 65)


# File Handling Functions
def load_inventory(inventory_obj):
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
                inventory_obj.products = []
                for item in data:
                    product_type = item.get("type", "physical")
                    if product_type == "physical":
                        product = PhysicalProduct(
                            item["id"], item["name"], item["price"], item["stock"], item.get("weight", 0.0)
                        )
                    elif product_type == "digital":
                        product = DigitalProduct(
                            item["id"], item["name"], item["price"], item["stock"], item.get("download_size", 0.0)
                        )
                    else:
                        continue
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

    data = [product.to_dict() for product in inventory_obj.products]
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully to inventory.json." if show_message else "Inventory saved successfully.")


# Main Menu & User Interaction
def main_menu():
    print("==============================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("==============================================\n")

    inventory = Inventory()
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
            print("Select Product Type:")
            print("1. Physical Product")
            print("2. Digital Product")
            type_choice = input("Enter choice (1/2): ").strip()

            if type_choice not in ["1", "2"]:
                print("Invalid type selected. Operation canceled.")
                continue

            product_id = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            price = float(input("Price: "))
            stock = int(input("Stock Quantity: "))

            if type_choice == "1":
                weight = float(input("Weight (kg): "))
                new_product = PhysicalProduct(product_id, name, price, stock, weight)
            else:
                download_size = float(input("Download Size (MB): "))
                new_product = DigitalProduct(product_id, name, price, stock, download_size)

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
                product.update_stock(new_stock)
                print("\nStock updated successfully!")
            else:
                print("\nProduct not found.")
        elif choice == "4":
            print("\nSearch Product")
            product_id = input("Enter Product ID: ").strip()

            product = inventory.search_product(product_id)
            if product:
                print("\nProduct Found")
                print("-" * 65)
                product.display_information()
                print(f"Fulfilment: {product.get_fulfilment_info()}")
                print("-" * 65)
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