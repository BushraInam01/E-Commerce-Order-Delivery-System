"""Tax abstractions for the final order calculation."""

from abc import ABC, abstractmethod


def _validate_non_negative_number(value, field_name):
    if value is True or value is False:
        raise TypeError(f"{field_name} must be a number.")
    try:
        numeric_value = value + 0
        is_negative = numeric_value < 0
    except (TypeError, ValueError):
        raise TypeError(f"{field_name} must be a number.") from None
    if is_negative:
        raise ValueError(f"{field_name} cannot be negative.")
    return numeric_value


class Tax(ABC):
    """Define the common interface for an Order tax calculation."""

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @abstractmethod
    def calculateTax(self, order):
        """Return a non-negative tax amount for an Order."""


class PercentageTax(Tax):
    """Calculate tax as a percentage of the product subtotal."""

    def __init__(self, percentage):
        super().__init__("Percentage Tax")
        percentage = _validate_non_negative_number(percentage, "Tax percentage")
        if percentage > 100:
            raise ValueError("Tax percentage cannot exceed 100.")
        self.__percentage = percentage

    @property
    def percentage(self):
        return self.__percentage

    def calculateTax(self, order):
        if order is None:
            raise ValueError("Order cannot be None.")
        return order.calculateSubtotal() * self.__percentage / 100


class FixedTax(Tax):
    """Apply a fixed non-negative tax amount to an Order."""

    def __init__(self, amount):
        super().__init__("Fixed Tax")
        self.__amount = _validate_non_negative_number(amount, "Fixed tax amount")

    @property
    def amount(self):
        return self.__amount

    def calculateTax(self, order):
        if order is None:
            raise ValueError("Order cannot be None.")
        return self.__amount
