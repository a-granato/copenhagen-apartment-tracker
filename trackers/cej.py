import requests
from bs4 import BeautifulSoup

from config import CEJ_URL


def test_cej_connection():

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
        )
    }

    response = requests.get(
        CEJ_URL,
        headers=headers,
        timeout=20
    )

    print(f"Status code: {response.status_code}")

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    print(f"Page title: {soup.title.text}")
