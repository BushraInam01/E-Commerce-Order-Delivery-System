"""Immutable invoice snapshots associated with orders."""

from datetime import datetime
from itertools import count


class Invoice:
    """Capture an Order's financial values at the time the invoice is issued."""

    _id_sequence = count(1)

    def __init__(self, order):
        self._validate_order(order)
        self.__invoice_id = f"INV{next(self._id_sequence):03d}"
        self.__order = order
        self.__issued_at = datetime.now()
        self.__subtotal = order.calculateSubtotal()
        self.__customer_discount = order.calculateCustomerDiscount()
        self.__discount = order.calculateDiscount()
        self.__order_total = order.calculateTotal()
        self.__delivery_cost = order.calculateShipping()
        self.__tax = order.calculateTax()
        self.__additional_charges = order.calculateAdditionalCharges()
        self.__final_total = order.calculateFinalTotal()

    @staticmethod
    def _validate_order(order):
        required_methods = (
            "calculateSubtotal",
            "calculateDiscount",
            "calculateCustomerDiscount",
            "calculateTotal",
            "calculateDeliveryCost",
            "calculateShipping",
            "calculateTax",
            "calculateAdditionalCharges",
            "calculateFinalTotal",
        )
        if order is None:
            raise ValueError("Order cannot be None.")
        if not hasattr(order, "order_id") or not hasattr(order, "customer"):
            raise TypeError("Invoice requires a valid Order.")
        if not all(callable(getattr(order, method, None)) for method in required_methods):
            raise TypeError("Invoice requires a valid Order.")

    @property
    def invoice_id(self):
        return self.__invoice_id

    @property
    def order(self):
        return self.__order

    @property
    def issued_at(self):
        return self.__issued_at

    @property
    def subtotal(self):
        return self.__subtotal

    @property
    def discount(self):
        return self.__discount

    @property
    def promotional_discount(self):
        return self.__discount

    @property
    def customer_discount(self):
        return self.__customer_discount

    @property
    def order_total(self):
        return self.__order_total

    @property
    def delivery_cost(self):
        return self.__delivery_cost

    @property
    def shipping(self):
        return self.__delivery_cost

    @property
    def tax(self):
        return self.__tax

    @property
    def additional_charges(self):
        return self.__additional_charges

    @property
    def final_total(self):
        return self.__final_total

    @property
    def total(self):
        """Return the final total using a concise invoice-facing name."""
        return self.__final_total

    def summary(self):
        """Return a safe invoice summary without payment credentials."""
        return (
            f"Invoice ID: {self.__invoice_id}\n"
            f"Order ID: {self.__order.order_id}\n"
            f"Customer: {self.__order.customer.name}\n"
            f"Invoice Date: {self.__issued_at.isoformat(timespec='seconds')}\n"
            f"Subtotal: {self.__subtotal}\n"
            f"Shipping: {self.__delivery_cost}\n"
            f"Tax: {self.__tax}\n"
            f"Customer Discount: {self.__customer_discount}\n"
            f"Promotional Discount: {self.__discount}\n"
            f"Additional Charges: {self.__additional_charges}\n"
            f"Final Total: {self.__final_total}"
        )
