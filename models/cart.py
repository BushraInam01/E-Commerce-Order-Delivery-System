"""Shopping-cart model for collecting products before an order is placed."""

from models.order import Order


class ShoppingCart:
    """Manage a customer's selected products through controlled operations."""

    def __init__(self, customer):
        if customer is None:
            raise ValueError("Customer cannot be None.")
        self.__customer = customer
        self.__items = {}

    @staticmethod
    def _validate_quantity(quantity):
        if type(quantity) is not int:
            raise TypeError("Quantity must be a whole number.")
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        return quantity

    @property
    def customer(self):
        return self.__customer

    def add_product(self, product, quantity):
        """Add a product or increase its existing cart quantity."""
        if product is None:
            raise ValueError("Product cannot be None.")
        quantity = self._validate_quantity(quantity)
        product_id = product.product_id
        if product_id in self.__items:
            self.__items[product_id][1] += quantity
        else:
            self.__items[product_id] = [product, quantity]

    def remove_product(self, product_id):
        """Remove a product or raise an error when it is absent."""
        if product_id not in self.__items:
            raise KeyError(f"Product {product_id!r} does not exist in the cart.")
        del self.__items[product_id]

    def calculate_total(self):
        """Calculate total through each product's polymorphic price method."""
        return sum(
            product.calculatePrice() * quantity
            for product, quantity in self.__items.values()
        )

    def get_items(self):
        """Return an immutable snapshot of (product, quantity) pairs."""
        return tuple(
            (product, quantity) for product, quantity in self.__items.values()
        )

    def clear(self):
        """Remove every cart item."""
        self.__items.clear()

    def place_order(self, order_id):
        """Atomically validate stock, create an Order, reduce stock, and clear."""
        if not self.__items:
            raise ValueError("Cannot place an order from an empty cart.")

        # Every product is checked before any stock is changed.
        for product, quantity in self.__items.values():
            product.validate_stock_availability(quantity)

        order = Order(order_id, self.__customer)
        for product, quantity in self.__items.values():
            order.addItem(product, quantity)

        for product, quantity in self.__items.values():
            product.reduce_stock_for_order(quantity)

        self.clear()
        return order
