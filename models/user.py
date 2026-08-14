"""User and administrator models for the e-commerce system."""


class User:
    """Represent a system user with controlled access to personal details."""

    def __init__(self, user_id, name, email):
        self.__user_id = self._validate_required_value(user_id, "User ID")
        self.name = name
        self.email = email

    @staticmethod
    def _validate_required_value(value, field_name):
        """Return a cleaned value or reject empty input."""
        cleaned_value = str(value).strip()
        if not cleaned_value:
            raise ValueError(f"{field_name} cannot be empty.")
        return cleaned_value

    @property
    def user_id(self):
        """Return the user's fixed identifier."""
        return self.__user_id

    @property
    def name(self):
        """Return the user's name."""
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = self._validate_required_value(value, "Name")

    @property
    def email(self):
        """Return the user's email address."""
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = self._validate_required_value(value, "Email")


class Admin(User):
    """Represent an administrator without future-phase management features."""

    def display_role(self):
        """Return the user's role."""
        return "Admin"
