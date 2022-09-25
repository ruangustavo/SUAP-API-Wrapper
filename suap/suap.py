from typing import Dict

import requests
from bs4 import BeautifulSoup

from urls import LOGIN_URL, PERSONAL_DATA_URL


class Suap:
    session = requests.Session()

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.session.headers["Referer"] = "https://suap.ifrn.edu.br/accounts/login/"

        if not self.login(username, password):
            raise ValueError("Invalid username or password")

    def get_csrf_token(self) -> str:
        """Get CSRF token from the SUAP website."""
        response = self.session.get(LOGIN_URL)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

    def login(self, username: str, password: str) -> None:
        """Login to the SUAP website."""
        data = {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": self.get_csrf_token(),
        }

        response = self.session.post(LOGIN_URL, data=data)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.find("p", class_="errornote") is None

    def get_personal_data(self) -> Dict[str, str]:
        """Get personal data from the SUAP website."""
        response = self.session.get(PERSONAL_DATA_URL.format(username=self.username))
        soup = BeautifulSoup(response.content, "html.parser")

        results = list(
            map(
                lambda s: s.text.strip(),
                soup.find_all("dd"),
            )
        )

        return {
            "name": results[0],
            "registration": results[1],
            "cpf": results[5],
            "rg": results[33],
            "email": results[3],
            "phone": results[50],
            "birth_date": results[16],
        }
