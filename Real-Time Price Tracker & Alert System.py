import requests
from bs4 import BeautifulSoup

def track_price(url, target_price):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    price = float(soup.find('span', class_='price').text.replace('$', ''))
    
    if price < target_price:
        send_email_alert(f"Price dropped to ${price}!")

# Track PS5 price on Amazon
track_price("https://amazon.com/ps5-listing", 499.99)
