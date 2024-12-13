class UserDoesNotExistException(Exception):
    """Raised when the user does not exist in the database."""

    pass


class EmailAlreadyExistsException(Exception):
    """Raised when an email is already registered."""

    pass


class InvalidPasswordException(Exception):
    """Raised when a provided password is incorrect."""

    pass
