from requests.auth import HTTPBasicAuth


class DocumentAuth:
    def __init__(self, user_name: str, password: str) -> None:
        self.user_name = user_name
        self.password = password

    @property
    def auth(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(self.user_name, self.password)
