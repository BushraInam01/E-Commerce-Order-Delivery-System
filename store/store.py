"""Store model demonstrating aggregation of independent Product objects."""


class Store:
    """Manage existing Products without owning or controlling their lifetimes."""

    def __init__(self, store_id, name):
        self.__store_id = self._validate_text(store_id, "Store ID")
        self.__name = self._validate_text(name, "Store name")
        self.__products = {}

    @staticmethod
    def _validate_text(value, field_name):
        cleaned_value = str(value).strip()
        if not cleaned_value:
            raise ValueError(f"{field_name} cannot be empty.")
        return cleaned_value

    @staticmethod
    def _validate_product(product):
        """Validate the common Product interface without concrete-type checks."""
        if product is None:
            raise ValueError("Product cannot be None.")
        required_attributes = ("product_id", "name")
        required_methods = ("calculatePrice", "requires_shipping")
        if not all(hasattr(product, attribute) for attribute in required_attributes):
            raise TypeError("Store requires a valid Product object.")
        if not all(callable(getattr(product, method, None)) for method in required_methods):
            raise TypeError("Store requires a valid Product object.")

    @property
    def store_id(self):
        return self.__store_id

    @property
    def name(self):
        return self.__name

    @property
    def products(self):
        """Return an immutable snapshot of the aggregated Products."""
        return tuple(self.__products.values())

    def add_product(self, product):
        """Aggregate an existing Product, rejecting duplicate product IDs."""
        self._validate_product(product)
        if product.product_id in self.__products:
            raise ValueError(
                f"Product {product.product_id!r} already exists in this store."
            )
        self.__products[product.product_id] = product

    def remove_product(self, product_id):
        """Remove and return a reference without destroying the Product."""
        if product_id not in self.__products:
            raise KeyError(f"Product {product_id!r} does not exist in this store.")
        return self.__products.pop(product_id)

    def get_product(self, product_id):
        """Return the aggregated Product matching product_id."""
        if product_id not in self.__products:
            raise KeyError(f"Product {product_id!r} does not exist in this store.")
        return self.__products[product_id]

    def list_products(self):
        """Return an immutable snapshot of all managed Products."""
        return tuple(self.__products.values())
