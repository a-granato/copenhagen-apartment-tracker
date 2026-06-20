import pandas as pd

from playwright.sync_api import sync_playwright

import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()


URL = "https://www.heimstaden.dk/ledige-lejeboliger/?search=2400&rent=1000%2C11000"


def get_heimstaden_urls():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(URL)

        page.wait_for_timeout(5000)

        apartments = page.locator(
            "a.rental-element"
        )

        urls = []

        for i in range(
            apartments.count()
        ):

            url = apartments.nth(i).get_attribute(
                "href"
            )

            if url.startswith("/"):
                url = (
                    "https://www.heimstaden.dk"
                    + url
                )

            urls.append(url)

        browser.close()

        return urls


def get_seen_urls():

    try:

        df = pd.read_csv(
            "data/seen_urls.csv"
        )

        return set(df["url"])

    except FileNotFoundError:

        return set()


def save_urls(urls):

    pd.DataFrame(
        {"url": list(urls)}
    ).to_csv(
        "data/seen_urls.csv",
        index=False
    )

def send_email(new_urls):

    if len(new_urls) == 0:
        return

    body = "\n\n".join(new_urls)

    msg = EmailMessage()

    msg["Subject"] = (
        f"{len(new_urls)} New Heimstaden Apartment(s)"
    )

    msg["From"] = os.getenv(
        "EMAIL_ADDRESS"
    )

    msg["To"] = os.getenv(
        "EMAIL_TO"
    )

    msg.set_content(body)

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            os.getenv("EMAIL_ADDRESS"),
            os.getenv("EMAIL_PASSWORD")
        )

        smtp.send_message(msg)

    print("Email sent successfully")

current_urls = set(
    get_heimstaden_urls()
)

seen_urls = get_seen_urls()

new_urls = current_urls - seen_urls

print(
    f"Found {len(new_urls)} new apartments"
)

for url in new_urls:

    print(url)

send_email(list(new_urls))

save_urls(current_urls)
