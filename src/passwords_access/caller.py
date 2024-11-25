from __future__ import annotations

from requests import Response

from . import config
from .auth import AuthBase, AuthText
from .dataclasses import CallerProps


class Caller:
    auth: AuthBase = AuthText

    def __init__(self, caller_props: CallerProps, auth: AuthBase | None = None) -> None:
        """
        Initialize the Caller object.

        Args:
            caller_props (CallerProps): The properties of the caller.
            auth (AuthBase | None, optional): The authentication object.
                Defaults to None.
        """

        self.caller_props = caller_props
        self.auth = (auth or self.auth)(caller_props)

    def __call__(self, url: str) -> Response:
        """
        Call the object as a function.

        Args:
            url (str): The URL to authenticate.

        Returns:
            Response: The response from the authentication.
        """

        return self.auth(url)

    def get_password(self, pk: str | int) -> Response:
        """
        Retrieves the password for the given primary key.

        Args:
            pk (str | int): The primary key of the password.

        Returns:
            Response: The response object containing the password.
        """

        return self.auth(f"{self.caller_props.url}{config.PASSWORDS_API}/{pk}")

    def get_passwords_list(self) -> Response:
        """
        Retrieves the list of passwords from the API.

        Returns:
            Response: The response object containing the list of passwords.
        """

        return self.auth(f"{self.caller_props.url}{config.PASSWORDS_API}")
