from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from constants import BASE_URL

LOGIN_ERROR_MESSAGE = "Por favor, entre com um usuário e senha corretos. Note que ambos os campos diferenciam maiúsculas e minúsculas."


class Suap:
    session = requests.Session()

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.session.headers["Referer"] = "https://suap.ifrn.edu.br/accounts/login/"

        if not self.login(username, password):
            raise ValueError(LOGIN_ERROR_MESSAGE)

    def get_csrf_token(self) -> str:
        """Get CSRF token from the SUAP website."""
        url = urljoin(BASE_URL, "accounts/login/")
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

    def login(self, username: str, password: str) -> None:
        """Login to the SUAP website."""
        url = urljoin(BASE_URL, "accounts/login/")

        data = {
            "csrfmiddlewaretoken": self.get_csrf_token(),
            "username": username,
            "password": password,
            "this_is_the_login_form": "1",
            "next": "/",
            "g-recaptcha-response": "",
        }

        response = self.session.post(url, data=data)
        return LOGIN_ERROR_MESSAGE not in response.text
