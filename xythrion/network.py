from typing import AnyStr, Optional, Union

from aiohttp import ClientSession

OUTPUT_OPTIONS = {
    "json": lambda r: r.json(),
    "html": lambda r: r.html(),
    "text": lambda r: r.text(),
}


class Network:
    """Methods requests/posts to the World Wide Web's Network."""

    def __init__(self, http_session: ClientSession) -> None:
        self.http_session = http_session

    async def request(self, url: str, output: Optional[str] = "json", **kwargs) -> Union[dict, AnyStr]:
        """Requesting from a URL."""
        async with self.http_session.get(url, **kwargs) as response:
            assert response.status == 200, f"Could not request from URL. Status {response.status}."

            return await OUTPUT_OPTIONS[output](response)

    async def post(self, url: str, output: Optional[str] = "json", **kwargs) -> Optional[Union[dict, AnyStr]]:
        """Posting data to a service."""
        async with self.http_session.post(url, **kwargs) as response:
            assert response.status == 200, f"Could not post to URL. Status {response.status}."

            return await OUTPUT_OPTIONS[output](response)
