"""Delivery-method hierarchy for the e-commerce system."""

from abc import ABC, abstractmethod


class DeliveryMethod(ABC):
    """Define the common interface for delivery cost and estimated time."""

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @staticmethod
    def _validate_order(order):
        if order is None:
            raise ValueError("Order cannot be None.")

    @abstractmethod
    def calculateCost(self, order):
        """Return delivery cost without product price, tax, or other charges."""

    @abstractmethod
    def getEstimatedDays(self):
        """Return a readable estimated delivery time."""


class StandardDelivery(DeliveryMethod):
    """Provide fixed-cost standard delivery in an estimated 3-5 days."""

    def __init__(self):
        super().__init__("Standard Delivery")
        self.__cost = 200

    @property
    def cost(self):
        return self.__cost

    def calculateCost(self, order):
        self._validate_order(order)
        return self.__cost

    def getEstimatedDays(self):
        return "3-5 days"


class ExpressDelivery(DeliveryMethod):
    """Provide fixed-cost express delivery in an estimated 1-2 days."""

    def __init__(self):
        super().__init__("Express Delivery")
        self.__cost = 500

    @property
    def cost(self):
        return self.__cost

    def calculateCost(self, order):
        self._validate_order(order)
        return self.__cost

    def getEstimatedDays(self):
        return "1-2 days"


class SameDayDelivery(DeliveryMethod):
    """Provide fixed-cost same-day delivery for the educational simulation."""

    def __init__(self):
        super().__init__("Same-Day Delivery")
        self.__cost = 1000

    @property
    def cost(self):
        return self.__cost

    def calculateCost(self, order):
        self._validate_order(order)
        return self.__cost

    def getEstimatedDays(self):
        return "Same day"
