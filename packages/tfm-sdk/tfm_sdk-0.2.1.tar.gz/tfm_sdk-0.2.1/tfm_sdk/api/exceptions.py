from aiohttp import ClientResponse


class TfmApiException(Exception):
    """Http api exception"""

    def __init__(self, r: ClientResponse, message: str | None = None):
        self.status_code = r.status
        self.r = r
        self.message = message or r.reason
        super().__init__(f"APIException: {message} (Status code: {self.status_code})")
