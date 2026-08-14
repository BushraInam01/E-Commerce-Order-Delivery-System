"""Customer models demonstrating inheritance and polymorphism."""

from abc import ABC, abstractmethod

from models.user import User


class Customer(User, ABC):
    """Define the common behavior required from every customer type."""

    @staticmethod
    def _validate_order_total(order_total):
        if not isinstance(order_total, (int, float)) or isinstance(order_total, bool):
            raise TypeError("Order total must be a number.")
        if order_total < 0:
            raise ValueError("Order total cannot be negative.")
        return order_total

    @abstractmethod
    def calculateDiscount(self, order_total):
        """Calculate and return this customer's discount amount."""

    @abstractmethod
    def has_free_shipping(self, order_total):
        """Return whether this customer receives free shipping."""

    @abstractmethod
    def display_role(self):
        """Return a readable customer role."""


class RegularCustomer(Customer):
    """A customer with no discount and no free shipping."""

    def calculateDiscount(self, order_total):
        self._validate_order_total(order_total)
        return 0.0

    def has_free_shipping(self, order_total):
        self._validate_order_total(order_total)
        return False

    def display_role(self):
        return "Regular Customer"


class PremiumCustomer(Customer):
    """A customer with a 10% discount and free shipping."""

    def calculateDiscount(self, order_total):
        order_total = self._validate_order_total(order_total)
        return order_total * 0.10

    def has_free_shipping(self, order_total):
        self._validate_order_total(order_total)
        return True

    def display_role(self):
        return "Premium Customer"


class BusinessCustomer(Customer):
    """A customer with a 15% discount and threshold-based free shipping."""

    # Until orders exist, the supplied total represents the shipping rule.
    FREE_SHIPPING_THRESHOLD = 5000

    def calculateDiscount(self, order_total):
        order_total = self._validate_order_total(order_total)
        return order_total * 0.15

    def has_free_shipping(self, order_total):
        order_total = self._validate_order_total(order_total)
        return order_total >= self.FREE_SHIPPING_THRESHOLD

    def display_role(self):
        return "Business Customer"
