from urllib.parse import urljoin

BASE_URL = "https://suap.ifrn.edu.br"
LOGIN_URL = urljoin(BASE_URL, "accounts/login/")
PERSONAL_DATA_URL = urljoin(BASE_URL, "edu/aluno/{username}/?tab=dados_pessoais")
