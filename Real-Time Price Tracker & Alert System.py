import requests
from bs4 import BeautifulSoup

def send_email_alert(message):
    # TODO(placeholder): this only prints the alert. To send a real email,
    # wire this up to smtplib (or an email API) with credentials read from
    # environment variables -- do not hard-code passwords here.
    print(f"[PRICE ALERT] {message}")

def track_price(url, target_price):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    price = float(soup.find('span', class_='price').text.replace('$', ''))
    
    if price < target_price:
        send_email_alert(f"Price dropped to ${price}!")

# Track PS5 price on Amazon
# REPAIR: moved under __main__ so importing this file no longer fires a live
# request at the placeholder URL. Replace the URL with a real product page
# before running -- "amazon.com/ps5-listing" is a placeholder, not a listing.
if __name__ == "__main__":
    track_price("https://amazon.com/ps5-listing", 499.99)
