"""

This script tracks and scrapes the prize of an item on
Amazon, sending an email notification when the price has dropped.

This script requires that 'requests', 'bs4',
'lxml', 'html', 'smtplib', 'python_dotenv'
be installed within the Python
environment you are running this script in.

"""

from bs4 import BeautifulSoup
import requests
import lxml
import html
import smtplib
from dotenv import load_dotenv
import os

load_dotenv('.env')
GMAIL_USERNAME = os.getenv('GMAIL_USERNAME')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
AMAZON_URL = 'https://www.amazon.ca/Nintendo-Switch-Neon-Blue-Joy%E2%80%91/dp/B084DDDNRP/ref=sr_1_3?dchild=1&keywords=nintendo%2Bswitch&qid=1615144805&sr=8-3&th=1'
PRICE_LIMIT = 700

MY_HEADERS = {
    'Accept-Language': os.getenv('Accept-Language'),
    'User-Agent': os.getenv('User-Agent')
}

response = requests.get(url=AMAZON_URL, headers=MY_HEADERS)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')

price_element = soup.find(name='span', id='priceblock_ourprice')
price = float(html.unescape(price_element.getText().split('$')[1]).strip())

if price < PRICE_LIMIT:
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=GMAIL_USERNAME, password=GMAIL_PASSWORD)
        connection.sendmail(from_addr=GMAIL_USERNAME, to_addrs='linglee2004@hotmail.com', msg=f'Subject:Low Price Alert!\n\n '
                                                                                              f'Hey, the price is currently ${price}. That is ${PRICE_LIMIT-price} below the price limit of ${PRICE_LIMIT}.')