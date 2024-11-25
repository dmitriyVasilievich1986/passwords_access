from __future__ import annotations

import re
from abc import ABC, abstractmethod
from enum import Enum

from requests import Response, request
from requests.cookies import RequestsCookieJar

from . import config
from .dataclasses import CallerProps, PostData


class RequestMethod(Enum):
    POST = "post"
    GET = "get"


class AuthBase(ABC):
    cookies: RequestsCookieJar | None = None
    timeout: int = 30

    def __init__(self, caller_props: CallerProps) -> None:
        """
        Initializes an instance of the Auth class.

        Args:
            caller_props (CallerProps): The properties of the caller.
        """

        self.caller_props = caller_props
        self._login()

    def __call__(self, url: str) -> Response:
        """
        Makes a GET request to the specified URL using the stored cookies.
        If the response status code is not 200, it will attempt
        to login and make the request again.

        Args:
            url (str): The URL to make the request to.

        Returns:
            Response: The response object from the GET request.
        """

        r = self.send_request(url)
        if r.status_code != 200:
            self._login()
            r = self.send_request(url)
        return r

    def _login(self) -> None:
        """
        Logs in the user by sending a POST request to the login URL
        with the provided username, password, and CSRF token.

        Raises:
            - SomeException: If there is an error during the login process.
        """

        response = self.send_request(url=f"{self.caller_props.url}{config.LOGIN_URL}")
        self.token = self.parse_csrf_token(response)

        data: PostData = PostData(
            username=self.caller_props.username,
            password=self.caller_props.password,
            csrf_token=self.token,
        )
        self.send_request(
            url=f"{self.caller_props.url}{config.LOGIN_URL}",
            method=RequestMethod.POST,
            data=data.json(),
        )

    def send_request(
        self,
        url: str,
        method: RequestMethod = RequestMethod.GET,
        data: dict | None = None,
    ) -> Response:
        """
        Sends a request to the specified URL using the specified method and data.

        Args:
            url (str): The URL to send the request to.
            method (RequestMethod, optional): The HTTP method to use for the request.
                Defaults to RequestMethod.GET.
            data (dict | None, optional): The data to send with the request.
                Defaults to None.

        Returns:
            Response: The response object containing the server's response
                to the request.
        """

        response: Response = request(
            cookies=self.cookies,
            timeout=self.timeout,
            method=method.value,
            data=data,
            url=url,
        )
        self.cookies = response.cookies or self.cookies
        return response

    @staticmethod
    @abstractmethod
    def parse_csrf_token(response: Response) -> str:
        """
        Parses the CSRF token from the given response.

        Args:
            response (Response): The response object from which
                to extract the CSRF token.

        Returns:
            str: The CSRF token extracted from the response.

        Raises:
            NotImplementedError: This method is not implemented
                and should be overridden in a subclass.
        """


class AuthText(AuthBase):  # pylint: disable=too-few-public-methods
    @staticmethod
    def parse_csrf_token(response: Response) -> str:
        """
        Parses the CSRF token from the given response.

        Args:
            response (Response): The response object containing the HTML.

        Returns:
            str: The CSRF token extracted from the HTML.

        Examples:
            >>> print(response.text)
            '<input id="csrf_token" name="csrf_token" type="hidden" value="reasonable_token">'
            >>> AuthText()._parse_csrf_token(response)
            'reasonable_token'
        """  # noqa: E501, pylint: disable=line-too-long

        input_value_reg = re.search(r'<input id="csrf_token".+?>', response.text)
        if input_value_reg is None:
            raise ValueError("CSRF token not found in response.")
        return re.sub(r'^<.+?value="|">$', "", input_value_reg.group(0))
