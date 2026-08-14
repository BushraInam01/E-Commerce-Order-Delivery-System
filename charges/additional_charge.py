"""Validated additional-charge value object."""


class AdditionalCharge:
    """Represent one named, immutable charge separate from shipping and tax."""

    def __init__(self, name, amount):
        cleaned_name = str(name).strip()
        if not cleaned_name:
            raise ValueError("Additional charge name cannot be empty.")
        if amount is True or amount is False:
            raise TypeError("Additional charge amount must be a number.")
        try:
            numeric_amount = amount + 0
            is_negative = numeric_amount < 0
        except (TypeError, ValueError):
            raise TypeError("Additional charge amount must be a number.") from None
        if is_negative:
            raise ValueError("Additional charge amount cannot be negative.")
        self.__name = cleaned_name
        self.__amount = numeric_amount

    @property
    def name(self):
        return self.__name

    @property
    def amount(self):
        return self.__amount
