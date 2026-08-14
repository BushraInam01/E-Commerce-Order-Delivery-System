"""Order and order-item models for the e-commerce system."""


class OrderItem:
    """Represent a product and quantity composed within an Order."""

    def __init__(self, product, quantity):
        if product is None:
            raise ValueError("Product cannot be None.")
        self.__product = product
        self.__quantity = self._validate_quantity(quantity)

    @staticmethod
    def _validate_quantity(quantity):
        if type(quantity) is not int:
            raise TypeError("Quantity must be a whole number.")
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        return quantity

    @property
    def product(self):
        return self.__product

    @property
    def quantity(self):
        return self.__quantity

    def increase_quantity(self, quantity):
        """Increase quantity through a validated operation."""
        self.__quantity += self._validate_quantity(quantity)

    def calculate_subtotal(self):
        """Delegate product pricing and multiply it by the quantity."""
        return self.__product.calculatePrice() * self.__quantity


class Order:
    """Own and manage OrderItem objects through Composition."""

    CREATED = "CREATED"
    UNPAID = "UNPAID"
    PAID = "PAID"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"

    def __init__(self, order_id, customer):
        cleaned_order_id = str(order_id).strip()
        if not cleaned_order_id:
            raise ValueError("Order ID cannot be empty.")
        if customer is None:
            raise ValueError("Customer cannot be None.")
        self.__order_id = cleaned_order_id
        self.__customer = customer
        self.__items = []
        self.__status = self.CREATED
        self.__discount = None
        self.__payment_method = None
        self.__payment_status = self.UNPAID
        self.__amount_paid = 0.0
        self.__amount_refunded = 0.0
        self.__delivery_method = None
        self.__tax = None
        self.__additional_charges = {}

    @property
    def order_id(self):
        return self.__order_id

    @property
    def customer(self):
        """Return the associated Customer."""
        return self.__customer

    @property
    def status(self):
        """Return the read-only order lifecycle status."""
        return self.__status

    @property
    def discount(self):
        """Return the selected order-level promotional discount, if any."""
        return self.__discount

    @property
    def payment_method(self):
        """Return the assigned PaymentMethod, if one has been selected."""
        return self.__payment_method

    @property
    def payment_status(self):
        return self.__payment_status

    @property
    def amount_paid(self):
        return self.__amount_paid

    @property
    def amount_refunded(self):
        return self.__amount_refunded

    @property
    def remaining_refundable_amount(self):
        return self.__amount_paid - self.__amount_refunded

    @property
    def delivery_method(self):
        """Return the selected DeliveryMethod, if one has been assigned."""
        return self.__delivery_method

    @property
    def items(self):
        """Return a read-only snapshot of the composed OrderItems."""
        return tuple(self.__items)

    @property
    def tax(self):
        """Return the selected Tax abstraction, if assigned."""
        return self.__tax

    @property
    def additional_charges(self):
        """Return an immutable snapshot of separately configured charges."""
        return tuple(self.__additional_charges.values())

    @staticmethod
    def _validate_financial_amount(value, field_name):
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

    def addItem(self, product, quantity):
        """Create and own an OrderItem, or merge a matching product quantity."""
        new_item = OrderItem(product, quantity)
        for item in self.__items:
            if item.product.product_id == product.product_id:
                item.increase_quantity(quantity)
                return
        self.__items.append(new_item)

    def removeItem(self, product_id):
        """Remove the item matching product_id or raise an error."""
        for item in self.__items:
            if item.product.product_id == product_id:
                self.__items.remove(item)
                return
        raise KeyError(f"Product {product_id!r} does not exist in the order.")

    def clearItems(self):
        """Clear the composed OrderItems through an Order-controlled operation."""
        self.__items.clear()

    def calculateSubtotal(self):
        """Calculate the subtotal by delegating to composed OrderItems."""
        subtotal = sum(item.calculate_subtotal() for item in self.__items)
        return self._validate_financial_amount(subtotal, "Product subtotal")

    def set_discount(self, discount):
        """Select one promotional Discount, or use None to remove it."""
        if discount is not None and not callable(getattr(discount, "applyDiscount", None)):
            raise TypeError("Discount must provide an applyDiscount(order) method.")
        self.__discount = discount

    def calculateDiscount(self):
        """Delegate promotional discount calculation to the selected object."""
        if self.__discount is None:
            return 0.0
        amount = self._validate_financial_amount(
            self.__discount.applyDiscount(self), "Promotional discount"
        )
        return min(amount, self.calculateSubtotal())

    def calculateCustomerDiscount(self):
        """Delegate customer discount behavior and cap it at the subtotal."""
        amount = self._validate_financial_amount(
            self.__customer.calculateDiscount(self.calculateSubtotal()),
            "Customer discount",
        )
        return min(amount, self.calculateSubtotal())

    def calculateTotal(self):
        """Return subtotal minus promotion, never less than zero."""
        return max(0.0, self.calculateSubtotal() - self.calculateDiscount())

    def set_delivery_method(self, delivery_method):
        """Assign a valid DeliveryMethod through a controlled operation."""
        if delivery_method is None:
            raise ValueError("Delivery method cannot be None.")
        calculate_cost = getattr(delivery_method, "calculateCost", None)
        estimated_days = getattr(delivery_method, "getEstimatedDays", None)
        if not callable(calculate_cost) or not callable(estimated_days):
            raise TypeError(
                "Delivery method must provide calculateCost() and getEstimatedDays()."
            )
        self.__delivery_method = delivery_method

    def calculateDeliveryCost(self):
        """Delegate delivery cost calculation, or return zero when unassigned."""
        if self.__delivery_method is None:
            return 0.0
        cost = self.__delivery_method.calculateCost(self)
        if type(cost) not in (int, float) or cost < 0:
            raise ValueError("Delivery cost must be a non-negative number.")
        return cost

    def calculateShipping(self):
        """Return shipping as a clearly named final-calculation component."""
        return self.calculateDeliveryCost()

    def set_tax(self, tax):
        """Assign one Tax abstraction, or use None to clear tax."""
        if tax is not None and not callable(getattr(tax, "calculateTax", None)):
            raise TypeError("Tax must provide calculateTax(order).")
        self.__tax = tax

    def calculateTax(self):
        """Delegate tax calculation, or return zero when tax is unassigned."""
        if self.__tax is None:
            return 0.0
        return self._validate_financial_amount(
            self.__tax.calculateTax(self), "Tax amount"
        )

    def add_additional_charge(self, charge):
        """Add a validated named charge without mixing it with shipping or tax."""
        if charge is None:
            raise ValueError("Additional charge cannot be None.")
        if not hasattr(charge, "name") or not hasattr(charge, "amount"):
            raise TypeError("A valid AdditionalCharge is required.")
        amount = self._validate_financial_amount(
            charge.amount, "Additional charge amount"
        )
        if charge.name in self.__additional_charges:
            raise ValueError(f"Additional charge {charge.name!r} already exists.")
        if amount != charge.amount:
            raise ValueError("Additional charge amount is invalid.")
        self.__additional_charges[charge.name] = charge

    def remove_additional_charge(self, name):
        """Remove and return a named additional charge."""
        if name not in self.__additional_charges:
            raise KeyError(f"Additional charge {name!r} does not exist.")
        return self.__additional_charges.pop(name)

    def calculateAdditionalCharges(self):
        """Return the sum of all separately configured additional charges."""
        total = sum(charge.amount for charge in self.__additional_charges.values())
        return self._validate_financial_amount(total, "Additional charges")

    def getEstimatedDeliveryDays(self):
        """Delegate the estimate, or return None when delivery is unassigned."""
        if self.__delivery_method is None:
            return None
        return self.__delivery_method.getEstimatedDays()

    def calculateFinalTotal(self):
        """Return the complete teacher-required final financial amount."""
        final_amount = (
            self.calculateSubtotal()
            + self.calculateShipping()
            + self.calculateTax()
            - self.calculateCustomerDiscount()
            - self.calculateDiscount()
            + self.calculateAdditionalCharges()
        )
        return max(0.0, final_amount)

    def set_payment_method(self, payment_method):
        """Assign a PaymentMethod before payment, or use None to clear it."""
        if self.__payment_status != self.UNPAID:
            raise ValueError("Payment method cannot be changed after payment.")
        if payment_method is not None:
            pay_method = getattr(payment_method, "pay", None)
            refund_method = getattr(payment_method, "refund", None)
            if not callable(pay_method) or not callable(refund_method):
                raise TypeError("Payment method must provide pay() and refund().")
        self.__payment_method = payment_method

    def pay(self):
        """Pay the complete final amount through the assigned PaymentMethod."""
        if self.__payment_method is None:
            raise ValueError("A payment method must be assigned before payment.")
        if self.__payment_status != self.UNPAID:
            raise ValueError("This order has already been paid.")
        amount = self.calculateFinalTotal()
        if amount <= 0:
            raise ValueError("Order payment amount must be greater than zero.")

        result = self.__payment_method.pay(amount)
        self.__amount_paid = amount
        self.__payment_status = self.PAID
        return result

    def refund(self, amount):
        """Refund a positive amount without exceeding the remaining payment."""
        if self.__payment_status == self.UNPAID:
            raise ValueError("The order must be paid before a refund.")
        if type(amount) not in (int, float):
            raise TypeError("Refund amount must be a number.")
        if amount <= 0:
            raise ValueError("Refund amount must be greater than zero.")
        if amount > self.remaining_refundable_amount:
            raise ValueError("Refund exceeds the remaining refundable amount.")

        result = self.__payment_method.refund(amount)
        self.__amount_refunded += amount
        if self.__amount_refunded == self.__amount_paid:
            self.__payment_status = self.REFUNDED
        return result

    def _require_status(self, required_status, action):
        """Reject a lifecycle action unless the order is in its required state."""
        if self.__status != required_status:
            raise ValueError(
                f"Cannot {action} an order with status {self.__status}; "
                f"required status is {required_status}."
            )

    def mark_paid(self):
        """Move CREATED to PAID only after successful, non-refunded payment."""
        self._require_status(self.CREATED, "mark as paid")
        if self.__payment_status != self.PAID:
            raise ValueError("Order payment status must be PAID before this transition.")
        self.__status = self.PAID

    def start_processing(self):
        """Move PAID to PROCESSING."""
        self._require_status(self.PAID, "start processing")
        self.__status = self.PROCESSING

    def ship(self):
        """Move PROCESSING to SHIPPED when a delivery method is assigned."""
        self._require_status(self.PROCESSING, "ship")
        if self.__delivery_method is None:
            raise ValueError("A delivery method must be assigned before shipping.")
        self.__status = self.SHIPPED

    def deliver(self):
        """Move SHIPPED to the terminal DELIVERED state."""
        self._require_status(self.SHIPPED, "deliver")
        self.__status = self.DELIVERED

    def cancel(self):
        """Cancel before shipping without automatically refunding payment."""
        cancellable_statuses = (self.CREATED, self.PAID, self.PROCESSING)
        if self.__status not in cancellable_statuses:
            raise ValueError(f"Cannot cancel an order with status {self.__status}.")
        self.__status = self.CANCELLED

    def generate_invoice(self):
        """Create an Invoice snapshot without embedding invoice logic in Order."""
        from invoices.invoice import Invoice

        return Invoice(self)

    def create_refund(self, amount, reason):
        """Create a pending Refund record; processing remains its responsibility."""
        from refunds.refund import Refund

        return Refund(self, amount, reason)

    def get_items(self):
        """Return a read-only snapshot of the internal item collection."""
        return tuple(self.__items)
