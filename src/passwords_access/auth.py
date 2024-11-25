import re
from abc import ABC, abstractmethod

import requests
from requests import Response

from . import config
from .dataclasses import CallerProps, PostData


class AuthBase(ABC):
    cookies: dict = None
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

        r = self.get_request(url)
        if r.status_code != 200:
            self._login()
            r = self.get_request(url)
        return r

    def _login(self) -> None:
        """
        Performs the login process.
        This method sends a GET request to retrieve the login page,
        and then sends a POST request with the login credentials.
        """

        response = self.get_request(url=f"{self.caller_props.url}{config.LOGIN_URL}")
        self.token = self._parse_csrf_token(response)
        self._post_request()

    def get_request(self, url: str) -> Response:
        """
        Sends a GET request to the specified URL and stores the response cookies.

        Args:
            url (str): The URL to send the request to.
        """

        response: Response = requests.get(
            headers={"content-type": "application/json"},
            cookies=self.cookies,
            timeout=self.timeout,
            url=url,
        )
        self.cookies = response.cookies
        return response

    def _post_request(self) -> Response:
        """
        Sends a POST request to the specified URL with the provided username,
            password, and CSRF token.

        Returns:
            Response: The response object containing the server's response
                to the request.
        """

        data: PostData = PostData(
            username=self.caller_props.username,
            password=self.caller_props.password,
            csrf_token=self.token,
        )
        r = requests.post(
            url=f"{self.caller_props.url}{config.LOGIN_URL}",
            cookies=self.cookies,
            timeout=self.timeout,
            data=data.json(),
        )
        self.cookies = r.cookies

    @abstractmethod
    def _parse_csrf_token(self, response: Response) -> str:
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

        raise NotImplementedError


class AuthText(AuthBase):  # pylint: disable=too-few-public-methods
    def _parse_csrf_token(self, response: Response) -> str:
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

        input_value = re.search(r'<input id="csrf_token".+?>', response.text).group(0)
        return re.sub(r'^<.+?value="|">$', "", input_value)
