"""Product hierarchy for the e-commerce system."""

from abc import ABC, abstractmethod


class Product(ABC):
    """Define shared product data and the common product interface."""

    def __init__(self, product_id, name, description, base_price):
        self.__product_id = self._validate_required_text(product_id, "Product ID")
        self.name = name
        self.description = description
        self.base_price = base_price

    @staticmethod
    def _validate_required_text(value, field_name):
        cleaned_value = str(value).strip()
        if not cleaned_value:
            raise ValueError(f"{field_name} cannot be empty.")
        return cleaned_value

    @staticmethod
    def _validate_number(value, field_name, allow_zero=True):
        if type(value) not in (int, float):
            raise TypeError(f"{field_name} must be a number.")
        if value < 0 or (not allow_zero and value == 0):
            rule = "zero or greater" if allow_zero else "greater than zero"
            raise ValueError(f"{field_name} must be {rule}.")
        return value

    @staticmethod
    def _validate_quantity(quantity):
        if type(quantity) is not int:
            raise TypeError("Quantity must be a whole number.")
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        return quantity

    @property
    def product_id(self):
        """Return the product's fixed identifier."""
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = self._validate_required_text(value, "Name")

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = self._validate_required_text(value, "Description")

    @property
    def base_price(self):
        return self.__base_price

    @base_price.setter
    def base_price(self, value):
        self.__base_price = self._validate_number(value, "Base price")

    @abstractmethod
    def calculatePrice(self):
        """Return the price according to the concrete product's rule."""

    @abstractmethod
    def requires_shipping(self):
        """Return whether the product needs physical shipping."""

    def validate_stock_availability(self, quantity):
        """Validate an order quantity; non-stocked products are always available."""
        self._validate_quantity(quantity)

    def reduce_stock_for_order(self, quantity):
        """Provide a stock hook; non-stocked products need no stock change."""
        self._validate_quantity(quantity)


class PhysicalProduct(Product):
    """Represent a stocked product that requires physical shipping."""

    def __init__(
        self, product_id, name, description, base_price, stock, weight, dimensions
    ):
        super().__init__(product_id, name, description, base_price)
        self.__stock = self._validate_stock(stock)
        self.weight = weight
        self.dimensions = dimensions

    @staticmethod
    def _validate_stock(value):
        if type(value) is not int:
            raise TypeError("Stock must be a whole number.")
        if value < 0:
            raise ValueError("Stock cannot be negative.")
        return value

    @property
    def stock(self):
        """Return current stock; changes use the controlled stock methods."""
        return self.__stock

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        self.__weight = self._validate_number(value, "Weight", allow_zero=False)

    @property
    def dimensions(self):
        return self.__dimensions

    @dimensions.setter
    def dimensions(self, value):
        self.__dimensions = self._validate_required_text(value, "Dimensions")

    def reduce_stock(self, quantity):
        """Remove an available quantity without allowing negative stock."""
        quantity = self._validate_quantity(quantity)
        if quantity > self.__stock:
            raise ValueError("Not enough stock available.")
        self.__stock -= quantity

    def increase_stock(self, quantity):
        """Add a positive quantity to stock."""
        self.__stock += self._validate_quantity(quantity)

    def validate_stock_availability(self, quantity):
        """Reject an order quantity greater than the available stock."""
        quantity = self._validate_quantity(quantity)
        if quantity > self.__stock:
            raise ValueError(f"Not enough stock available for {self.name}.")

    def reduce_stock_for_order(self, quantity):
        """Reduce stock after the cart has validated every product."""
        self.reduce_stock(quantity)

    def calculatePrice(self):
        """Return base price; delivery charges belong to a future phase."""
        return self.base_price

    def requires_shipping(self):
        return True


class DigitalProduct(Product):
    """Represent a non-physical product accessed through a download URL."""

    def __init__(self, product_id, name, description, base_price, download_url):
        super().__init__(product_id, name, description, base_price)
        self.download_url = download_url

    @property
    def download_url(self):
        return self.__download_url

    @download_url.setter
    def download_url(self, value):
        self.__download_url = self._validate_required_text(value, "Download URL")

    def calculatePrice(self):
        return self.base_price

    def requires_shipping(self):
        return False


class SubscriptionProduct(Product):
    """Represent a recurring product with optional automatic renewal."""

    def __init__(
        self,
        product_id,
        name,
        description,
        base_price,
        subscription_duration,
        auto_renew,
    ):
        super().__init__(product_id, name, description, base_price)
        self.subscription_duration = subscription_duration
        self.auto_renew = auto_renew

    @property
    def subscription_duration(self):
        """Return the subscription duration in months."""
        return self.__subscription_duration

    @subscription_duration.setter
    def subscription_duration(self, value):
        if type(value) is not int:
            raise TypeError("Subscription duration must be a whole number of months.")
        if value <= 0:
            raise ValueError("Subscription duration must be positive.")
        self.__subscription_duration = value

    @property
    def auto_renew(self):
        return self.__auto_renew

    @auto_renew.setter
    def auto_renew(self, value):
        if type(value) is not bool:
            raise TypeError("Auto renew must be a boolean.")
        self.__auto_renew = value

    def calculatePrice(self):
        """Return the recurring price for one subscription period."""
        return self.base_price

    def requires_shipping(self):
        return False

    def renew(self):
        """Indicate whether automatic renewal will occur; no payment is processed."""
        return self.auto_renew
