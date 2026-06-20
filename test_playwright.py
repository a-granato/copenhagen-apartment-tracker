from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(
        "https://www.heimstaden.dk/ledige-lejeboliger/?search=2400&rent=1000%2C11000"
    )

    page.wait_for_timeout(5000)

    apartments = page.locator("a.rental-element")

    results = []

    for i in range(apartments.count()):

        apartment = apartments.nth(i)

        text = apartment.inner_text()

        url = apartment.get_attribute("href")

        if url.startswith("/"):
            url = f"https://www.heimstaden.dk{url}"

        results.append({
            "text": text,
            "url": url
        })

    browser.close()

    for apartment in results:

        print("\n====================")
        print(apartment["text"])
        print(apartment["url"])
