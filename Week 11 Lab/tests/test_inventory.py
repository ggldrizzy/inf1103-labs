import inspect
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inventory_manager import (
    BulkDiscount,
    DiscountStrategy,
    Inventory,
    NoDiscount,
    Order,
    OrderLine,
    PercentageDiscount,
    ProductFactory,
    StudentDiscount,
    Supplier,
    get_non_negative_int,
    get_positive_float,
    load_products,
)

SUPPLIER = Supplier("S1", "Acme", "a@b.com")


def make_order(discount=None) -> Order:
    """Order whose lines add up to 250."""
    order = Order("O1", discount)
    lamp = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, SUPPLIER, 1.0)
    order.add_order_line(lamp, 10)
    return order


# ---------- Strategy ----------
def test_default_is_no_discount():
    assert make_order().calculate_total() == 250


def test_bulk_discount_applies_over_threshold():
    assert make_order(BulkDiscount(200, 20)).calculate_total() == 230


def test_bulk_discount_not_applied_under_threshold():
    assert BulkDiscount(300, 20).apply(250) == 250


def test_set_discount_changes_strategy():
    order = make_order(BulkDiscount(200, 20))
    assert order.calculate_total() == 230
    order.set_discount(PercentageDiscount(10))
    assert order.calculate_total() == 225


def test_student_discount_added_without_changing_order():
    assert make_order(StudentDiscount()).calculate_total() == pytest.approx(237.5)


def test_new_strategy_works_with_unmodified_order():
    class HalfPrice(DiscountStrategy):
        def apply(self, total: float) -> float:
            return total / 2

    assert make_order(HalfPrice()).calculate_total() == 125


def test_order_has_no_discount_branching():
    source = inspect.getsource(Order)
    assert "if discount_type" not in source
    assert "elif" not in source


def test_no_discount_returns_total_unchanged():
    assert NoDiscount().apply(99.5) == 99.5


# ---------- Factory ----------
def test_factory_returns_correct_types():
    physical = ProductFactory.create("physical", "P1", "Lamp", 25.0, 1, SUPPLIER, 1.0)
    digital = ProductFactory.create("digital", "D1", "App", 10.0, 1, SUPPLIER, 5.0)
    assert type(physical).__name__ == "PhysicalProduct"
    assert type(digital).__name__ == "DigitalProduct"


def test_unknown_product_type_raises_clear_error():
    with pytest.raises(ValueError, match="Unknown product type: service"):
        ProductFactory.create("service", "S1", "Install", 30.0, 5, SUPPLIER)


# ---------- Validation ----------
@pytest.mark.parametrize("price", [0, -1])
def test_invalid_price_rejected(price):
    with pytest.raises(ValueError, match="Price"):
        ProductFactory.create("physical", "X", "X", price, 1, SUPPLIER)


def test_negative_stock_rejected():
    with pytest.raises(ValueError, match="Stock"):
        ProductFactory.create("digital", "X", "X", 5.0, -1, SUPPLIER)


def test_update_stock_rejects_negative_for_every_subclass():
    for kind in ("physical", "digital"):
        product = ProductFactory.create(kind, "X", "X", 5.0, 1, SUPPLIER)
        with pytest.raises(ValueError):
            product.update_stock(-5)


@pytest.mark.parametrize("quantity", [0, -3])
def test_invalid_order_quantity_rejected(quantity):
    product = ProductFactory.create("digital", "X", "X", 5.0, 1, SUPPLIER)
    with pytest.raises(ValueError, match="Quantity"):
        OrderLine(product, quantity)


# ---------- User input ----------
def test_get_positive_float_retries_until_valid(monkeypatch, capsys):
    answers = iter(["abc", "-5", "12.50"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert get_positive_float("Price: ") == 12.5
    out = capsys.readouterr().out.splitlines()
    assert out == [
        "Please enter a valid number, e.g. 12.50",
        "Please enter a number greater than zero.",
    ]


def test_get_non_negative_int_retries_until_valid(monkeypatch):
    answers = iter(["x", "1.5", "-2", "7"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert get_non_negative_int("Stock: ") == 7


# ---------- CSV loading ----------
CSV_TEXT = (
    "product_type,product_id,name,price,stock_quantity\n"
    "physical,P001,Desk Lamp,25.00,10\n"
    "digital,D001,Photo Editor,49.90,100\n"
    "service,S001,Installation,30.00,5\n"
    "physical,P002,Office Chair,abc,3\n"
    "physical,P003,Monitor Stand,39.50,7\n"
)


def test_load_products_skips_bad_rows_and_keeps_good_ones(tmp_path, capsys):
    path = tmp_path / "products.csv"
    path.write_text(CSV_TEXT)
    inventory = Inventory()
    load_products(str(path), inventory, SUPPLIER)

    assert [p.product_id for p in inventory.products] == ["P001", "D001", "P003"]
    lines = capsys.readouterr().out.splitlines()
    assert "S001" in lines[0] and "Unknown product type" in lines[0]
    assert "P002" in lines[1]
    assert lines[2] == "3 products loaded."
    assert lines[3] == "Load attempt finished."


def test_missing_file_handled_gracefully(capsys):
    inventory = Inventory()
    load_products("does_not_exist.csv", inventory, SUPPLIER)
    out = capsys.readouterr().out.splitlines()
    assert out == ["Products file not found: does_not_exist.csv", "Load attempt finished."]
    assert inventory.products == []
