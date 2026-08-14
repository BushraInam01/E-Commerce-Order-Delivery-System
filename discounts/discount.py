"""Promotional discount hierarchy for orders."""

from abc import ABC, abstractmethod


def _validate_percentage(value):
    """Validate a percentage shared by percentage-based promotions."""
    if type(value) not in (int, float):
        raise TypeError("Percentage must be a number.")
    if value < 0 or value > 100:
        raise ValueError("Percentage must be between 0 and 100.")
    return value


class Discount(ABC):
    """Define the interface for an order-level promotional discount."""

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        """Return a readable, immutable promotion name."""
        return self.__name

    @abstractmethod
    def applyDiscount(self, order):
        """Return the discount amount for an order, not its final total."""


class PercentageDiscount(Discount):
    """Discount an order subtotal by a configured percentage."""

    def __init__(self, percentage):
        super().__init__("Percentage Discount")
        self.__percentage = _validate_percentage(percentage)

    @property
    def percentage(self):
        return self.__percentage

    def applyDiscount(self, order):
        return order.calculateSubtotal() * self.__percentage / 100


class FixedAmountDiscount(Discount):
    """Discount a fixed amount, capped at the order subtotal."""

    def __init__(self, amount):
        super().__init__("Fixed Amount Discount")
        if type(amount) not in (int, float):
            raise TypeError("Fixed discount amount must be a number.")
        if amount < 0:
            raise ValueError("Fixed discount amount cannot be negative.")
        self.__amount = amount

    @property
    def amount(self):
        return self.__amount

    def applyDiscount(self, order):
        return min(self.__amount, order.calculateSubtotal())


class BuyOneGetOneDiscount(Discount):
    """Make one unit free for every pair of the same product in an order."""

    def __init__(self):
        super().__init__("Buy One Get One Discount")

    def applyDiscount(self, order):
        """Calculate free units as quantity // 2 for every OrderItem."""
        return sum(
            item.product.calculatePrice() * (item.quantity // 2)
            for item in order.get_items()
        )


class SeasonalDiscount(Discount):
    """Apply a configured percentage as the phase's date-free seasonal rule."""

    def __init__(self, percentage):
        super().__init__("Seasonal Discount")
        self.__percentage = _validate_percentage(percentage)

    @property
    def percentage(self):
        return self.__percentage

    def applyDiscount(self, order):
        return order.calculateSubtotal() * self.__percentage / 100
