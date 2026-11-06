import json
import os
from abc import ABC, abstractmethod

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(BASE_DIR, "inventory.json")


# ---------------------------------------------------------
# Supplier Class (Association with Product)
# ---------------------------------------------------------
class Supplier:
    """Represents a product supplier (Association relationship with Product)."""

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> None:
        """Displays supplier details."""
        print(f"Supplier ID: {self.supplier_id} | Name: {self.name} | Email: {self.contact_email}")

    def to_dict(self) -> dict:
        """Serializes supplier data."""
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_email": self.contact_email,
        }

    @staticmethod
    def from_dict(data: dict) -> "Supplier":
        """Deserializes supplier data."""
        return Supplier(
            supplier_id=data["supplier_id"],
            name=data["name"],
            contact_email=data["contact_email"],
        )


# ---------------------------------------------------------
# Interfaces & Product Hierarchy
# ---------------------------------------------------------
class CanBeShipped(ABC):
    """Interface contract for items that require physical shipping."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class Product(ABC):
    """Abstract Base Class for products."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self._product_id: str = product_id
        self.name: str = name
        self._price: float = price
        self._stock: int = stock
        self.supplier: Supplier = supplier  # Association: holds reference to Supplier

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    def update_stock(self, quantity: int) -> None:
        """Encapsulates stock modification behavior inside the class."""
        self._stock = quantity

    def display_information(self) -> None:
        """Displays base product information and supplier details."""
        print(
            f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock} | Supplier: {self.supplier.name}",
            end="",
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method to be implemented by concrete product subclasses."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Abstract method for dictionary serialization for JSON storage."""
        pass


class PhysicalProduct(Product, CanBeShipped):
    """Represents a physical product with weight and shipping capabilities."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.weight: float = float(weight)

    def display_information(self) -> None:
        super().display_information()
        print(f" | Weight: {self.weight}kg | Shipping: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self) -> str:
        return f"Product requires physical shipping. Weight: {self.weight}kg."

    def calculate_shipping_cost(self) -> float:
        return 5.00 + (self.weight * 2.00)

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "supplier": self.supplier.to_dict(),
            "weight": self.weight,
        }


class DigitalProduct(Product):
    """Represents a digital product delivered via digital download."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.download_size: float = float(download_size)

    def display_information(self) -> None:
        super().display_information()
        print(f" | Download Size: {self.download_size}MB")

    def get_fulfilment_info(self) -> str:
        return f"Product is delivered digitally. Download size: {self.download_size}MB."

    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "supplier": self.supplier.to_dict(),
            "download_size": self.download_size,
        }


# ---------------------------------------------------------
# Inventory Class (Aggregation with Product)
# ---------------------------------------------------------
class Inventory:
    """Manages a collection of Product instances (Aggregation relationship)."""

    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        """Adds a Product instance to the inventory."""
        self.products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        """Removes and returns a product from the inventory without destroying it."""
        product = self.find_product(product_id)
        if product:
            self.products.remove(product)
            return product
        return None

    def find_product(self, product_id: str) -> Product | None:
        """Finds and returns a product by ID, or None if not found."""
        for item in self.products:
            if item.product_id == product_id:
                return item
        return None

    def display_all(self) -> None:
        """Displays all products using polymorphic display_information method."""
        print("\nCurrent Inventory")
        print("-" * 75)
        if not self.products:
            print("Inventory is empty.")
        else:
            for item in self.products:
                item.display_information()
        print("-" * 75)


# ---------------------------------------------------------
# Order & OrderLine Classes (Composition relationship)
# ---------------------------------------------------------
class OrderLine:
    """Represents one product line item in an order (Owned by Order)."""

    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        """Calculates line item subtotal."""
        return self.product.price * self.quantity


class Order:
    """Manages an order and creates/owns its OrderLine instances (Composition)."""

    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Internal creation of OrderLine enforces Composition lifecycle ownership."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        """Calculates total order amount by summing line item subtotals."""
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order_details(self) -> None:
        """Prints order summary and line item details."""
        print(f"\nOrder ID: {self.order_id}")
        print("=" * 60)
        for line in self.order_lines:
            subtotal = line.calculate_subtotal()
            print(f"- {line.product.name} x {line.quantity} @ ${line.product.price:.2f} = ${subtotal:.2f}")
        print(f"Total Order Amount: ${self.calculate_total():.2f}")
        print("=" * 60)


# ---------------------------------------------------------
# Standalone LSP & Polymorphism Demonstrator Functions
# ---------------------------------------------------------
def show_product_details(product: Product) -> None:
    """LSP Verification Function: Demonstrates substitutability of any Product subclass."""
    product.display_information()
    print(f"\nFulfilment Info: {product.get_fulfilment_info()}")


# ---------------------------------------------------------
# File Handling Functions
# ---------------------------------------------------------
def load_inventory(inventory_obj: Inventory) -> None:
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
                inventory_obj.products = []
                for item in data:
                    product_type = item.get("type", "physical")
                    supplier_data = item.get("supplier", {"supplier_id": "SUP000", "name": "Generic Supplier", "contact_email": "info@supplier.com"})
                    supplier = Supplier.from_dict(supplier_data)

                    if product_type == "physical":
                        product = PhysicalProduct(
                            item["id"], item["name"], item["price"], item["stock"], supplier, item.get("weight", 0.0)
                        )
                    elif product_type == "digital":
                        product = DigitalProduct(
                            item["id"], item["name"], item["price"], item["stock"], supplier, item.get("download_size", 0.0)
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


def save_inventory(inventory_obj: Inventory, show_message: bool = True) -> None:
    if show_message:
        print("Saving inventory...")

    data = [product.to_dict() for product in inventory_obj.products]
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully to inventory.json." if show_message else "Inventory saved successfully.")


# ---------------------------------------------------------
# Main Menu & CLI Execution
# ---------------------------------------------------------
def main_menu() -> None:
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

            print("\nSupplier Information:")
            sup_id = input("Supplier ID: ").strip()
            sup_name = input("Supplier Name: ").strip()
            sup_email = input("Supplier Email: ").strip()
            supplier = Supplier(sup_id, sup_name, sup_email)

            if type_choice == "1":
                weight = float(input("Weight (kg): "))
                new_product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
            else:
                download_size = float(input("Download Size (MB): "))
                new_product = DigitalProduct(product_id, name, price, stock, supplier, download_size)

            inventory.add_product(new_product)
            print("\nProduct added successfully!")

        elif choice == "3":
            print("\nUpdate Stock")
            product_id = input("Enter Product ID: ").strip()

            product = inventory.find_product(product_id)
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

            product = inventory.find_product(product_id)
            if product:
                print("\nProduct Found")
                print("-" * 65)
                product.display_information()
                print(f"\nFulfilment: {product.get_fulfilment_info()}")
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