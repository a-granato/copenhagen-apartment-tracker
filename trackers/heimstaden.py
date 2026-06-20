import requests

from config import HEIMSTADEN_URL


def get_heimstaden_listings():

    response = requests.get(
        HEIMSTADEN_URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    print("Length:", len(response.text))
    print("Contains Dortheavej:", "Dortheavej" in response.text)

    position = response.text.find("Dortheavej")

    print("Position:", position)

    if position > -1:

        start = max(0, position - 500)
        end = position + 500

        print(response.text[start:end])

    return []
