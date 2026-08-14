"""Simulated payment-method hierarchy for the e-commerce system."""

from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    """Define the common interface for simulated payments and refunds."""

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @staticmethod
    def _validate_amount(amount):
        if type(amount) not in (int, float):
            raise TypeError("Payment amount must be a number.")
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        return amount

    @staticmethod
    def _validate_text(value, field_name):
        cleaned_value = str(value).strip()
        if not cleaned_value:
            raise ValueError(f"{field_name} cannot be empty.")
        return cleaned_value

    @classmethod
    def _validate_masked_identifier(cls, value, field_name):
        masked_value = cls._validate_text(value, field_name)
        if "*" not in masked_value:
            raise ValueError(f"{field_name} must be masked with * characters.")
        return masked_value

    @abstractmethod
    def pay(self, amount):
        """Simulate a successful payment and return a payment result."""

    @abstractmethod
    def refund(self, amount):
        """Simulate a successful refund and return a refund result."""


class CreditCard(PaymentMethod):
    """Simulate card payments while retaining only a masked card number."""

    def __init__(self, card_holder, masked_card_number):
        super().__init__("Credit Card")
        self.__card_holder = self._validate_text(card_holder, "Card holder")
        self.__masked_card_number = self._validate_masked_identifier(
            masked_card_number, "Masked card number"
        )

    @property
    def card_holder(self):
        return self.__card_holder

    @property
    def masked_card_number(self):
        return self.__masked_card_number

    def pay(self, amount):
        amount = self._validate_amount(amount)
        return {
            "status": "PAID",
            "method": self.name,
            "amount": amount,
            "message": "Credit card payment authorized.",
        }

    def refund(self, amount):
        amount = self._validate_amount(amount)
        return {
            "status": "REFUNDED",
            "method": self.name,
            "amount": amount,
            "message": "Credit card refund returned to the card.",
        }


class BankTransfer(PaymentMethod):
    """Simulate bank transfers using a masked account reference."""

    def __init__(self, bank_name, masked_account_reference):
        super().__init__("Bank Transfer")
        self.__bank_name = self._validate_text(bank_name, "Bank name")
        self.__masked_account_reference = self._validate_masked_identifier(
            masked_account_reference, "Masked account reference"
        )

    @property
    def bank_name(self):
        return self.__bank_name

    @property
    def masked_account_reference(self):
        return self.__masked_account_reference

    def pay(self, amount):
        amount = self._validate_amount(amount)
        return {
            "status": "PAID",
            "method": self.name,
            "amount": amount,
            "message": "Bank transfer confirmed.",
        }

    def refund(self, amount):
        amount = self._validate_amount(amount)
        return {
            "status": "REFUNDED",
            "method": self.name,
            "amount": amount,
            "message": "Bank transfer refund initiated.",
        }


class DigitalWallet(PaymentMethod):
    """Simulate wallet payments using a masked wallet identifier."""

    def __init__(self, wallet_name, masked_wallet_id):
        super().__init__("Digital Wallet")
        self.__wallet_name = self._validate_text(wallet_name, "Wallet name")
        self.__masked_wallet_id = self._validate_masked_identifier(
            masked_wallet_id, "Masked wallet ID"
        )

    @property
    def wallet_name(self):
        return self.__wallet_name

    @property
    def masked_wallet_id(self):
        return self.__masked_wallet_id

    def pay(self, amount):
        amount = self._validate_amount(amount)
        return {
            "status": "PAID",
            "method": self.name,
            "amount": amount,
            "message": "Digital wallet payment completed instantly.",
        }

    def refund(self, amount):
        amount = self._validate_amount(amount)
        return {
            "status": "REFUNDED",
            "method": self.name,
            "amount": amount,
            "message": "Digital wallet balance credited.",
        }
