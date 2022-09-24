from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from constants import BASE_URL


class Suap:
    session = requests.Session()

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.session.headers["Referer"] = "https://suap.ifrn.edu.br/accounts/login/"

        if not self.login(username, password):
            raise ValueError("Invalid username or password")

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
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.find("p", class_="errornote") is None
