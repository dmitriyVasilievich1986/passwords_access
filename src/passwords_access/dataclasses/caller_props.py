from dataclasses import asdict, dataclass


@dataclass
class CallerProps:
    username: str
    password: str
    host: str
    port: int

    @property
    def url(self) -> str:
        """
        Returns the URL formed by combining the host and port.

        Returns:
            str: The URL formed by combining the host and port.

        Examples:
            >>> caller_props = CallerProps("user", "pass", "localhost", 80)
            >>> caller_props.url
            'http://localhost:80'
        """

        return f"http://{self.host}:{self.port}"


@dataclass
class PostData:
    username: str
    password: str
    csrf_token: str

    def json(self) -> dict:
        """
        Returns the JSON representation of the caller_props object.

        Returns:
            dict: A dictionary representing the JSON data.
        """

        return asdict(self)
