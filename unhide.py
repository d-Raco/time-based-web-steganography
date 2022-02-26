
import requests
from time import time
from bs4 import BeautifulSoup

r = requests.get('http://localhost/Lab_Steganography/index.html')

soup = BeautifulSoup(r.text, 'html.parser')
msg = False

for item in soup.find_all('img'):
    r = requests.get('http://localhost/Lab_Steganography/' + item['src'])
    delay = int(r.elapsed.total_seconds() * 1000/12)

    if (delay == 2):
        msg = True
    elif (delay == 3):
        msg = False
        print()
        break
    elif (msg):
        print(chr(delay), end = "")
