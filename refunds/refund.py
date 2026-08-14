"""Refund records that coordinate with existing Order payment behavior."""

from itertools import count


class Refund:
    """Represent and track an explicit refund request associated with an Order."""

    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    _id_sequence = count(1)

    def __init__(self, order, amount, reason):
        self._validate_order(order)
        validated_amount = self._validate_amount(amount)
        cleaned_reason = str(reason).strip()
        if not cleaned_reason:
            raise ValueError("Refund reason cannot be empty.")
        self._validate_eligibility(order, validated_amount)

        self.__refund_id = f"REF{next(self._id_sequence):03d}"
        self.__order = order
        self.__amount = validated_amount
        self.__reason = cleaned_reason
        self.__status = self.PENDING
        self.__result = None

    @staticmethod
    def _validate_order(order):
        if order is None:
            raise ValueError("Order cannot be None.")
        required_attributes = (
            "payment_status",
            "amount_paid",
            "remaining_refundable_amount",
        )
        if not all(hasattr(order, attribute) for attribute in required_attributes):
            raise TypeError("Refund requires a valid Order.")
        if not callable(getattr(order, "refund", None)):
            raise TypeError("Refund requires a valid Order.")

    @staticmethod
    def _validate_amount(amount):
        if type(amount) not in (int, float):
            raise TypeError("Refund amount must be a number.")
        if amount <= 0:
            raise ValueError("Refund amount must be greater than zero.")
        return amount

    @staticmethod
    def _validate_eligibility(order, amount):
        if order.payment_status != order.PAID:
            raise ValueError("Refund requires an order with PAID payment status.")
        if amount > order.amount_paid:
            raise ValueError("Refund amount cannot exceed the amount paid.")
        if amount > order.remaining_refundable_amount:
            raise ValueError("Refund exceeds the remaining refundable amount.")

    @property
    def refund_id(self):
        return self.__refund_id

    @property
    def order(self):
        return self.__order

    @property
    def amount(self):
        return self.__amount

    @property
    def reason(self):
        return self.__reason

    @property
    def status(self):
        return self.__status

    @property
    def result(self):
        """Return a copy so callers cannot mutate the stored payment result."""
        if self.__result is None:
            return None
        return dict(self.__result)

    def process(self):
        """Validate and delegate the transaction to Order's payment workflow."""
        if self.__status != self.PENDING:
            raise ValueError("Only a PENDING refund can be processed.")
        try:
            self._validate_eligibility(self.__order, self.__amount)
            result = self.__order.refund(self.__amount)
        except Exception:
            self.__status = self.FAILED
            raise

        self.__result = dict(result)
        self.__status = self.COMPLETED
        return dict(self.__result)
