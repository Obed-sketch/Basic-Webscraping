import re

import requests
from bs4 import BeautifulSoup


def send_email_alert(message):
    # TODO(placeholder): this only prints the alert. To send a real email,
    # wire this up to smtplib (or an email API) with credentials read from
    # environment variables -- do not hard-code passwords here.
    print(f"[PRICE ALERT] {message}")


def _extract_price(soup):
    """Find a price on a product page, tolerating common markup variants.

    Tries, in order: a <span class="price"> (the original selector), any
    element whose class contains 'price' (e.g. books.toscrape.com's
    <p class="price_color">), then a currency-amount pattern in the text.
    Returns (price_as_float, currency_symbol) or (None, '').
    """
    el = soup.find('span', class_='price')
    if el is None:
        el = soup.find(class_=re.compile(r'price'))
    texts = [el.get_text()] if el is not None else []
    texts.append(soup.get_text())
    for text in texts:
        m = re.search(r'([$£€])\s*([0-9][0-9,]*\.?[0-9]*)', text)
        if m:
            return float(m.group(2).replace(',', '')), m.group(1)
    return None, ''


def track_price(url, target_price):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    price, symbol = _extract_price(soup)
    if price is None:
        print(f"Could not find a price on {url}")
        return None
    print(f"Current price: {symbol}{price:.2f} (target: {symbol}{target_price:.2f})")
    if price < target_price:
        send_email_alert(f"Price dropped to {symbol}{price:.2f}!")
    return price


if __name__ == "__main__":
    # DEMO TARGET (verified Nov 2026): books.toscrape.com is a public
    # sandbox shop built for scraping practice, so it is a stable,
    # no-auth demo page. The book "A Light in the Attic" is priced at
    # GBP 51.77 there; the target below is set just above that so the
    # alert path fires. To track a real product instead, pass any
    # product-page URL and target price to track_price().
    track_price(
        "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        55.00,
    )
