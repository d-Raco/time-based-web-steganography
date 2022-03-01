import requests
import globals
from time import time
from bs4 import BeautifulSoup

# Define global variables
globals.init_globals()

r = requests.get('http://localhost/Lab_Steganography/index.html')

soup = BeautifulSoup(r.text, 'html.parser')
msg = False
char_list = []
index = 0

for item in soup.find_all('img'):
    if (not msg and item['id'] == str(globals.images_per_char-1)):
        msg = True
    elif (msg):
        r = requests.get('http://localhost/Lab_Steganography/' + item['src'])
        delay = globals.dec_to_base((r.elapsed.total_seconds() * 1000/globals.inter_delay), globals.base)

        char_list.insert(0, delay)
        index += 1

        if (index % globals.images_per_char == 0):
            index = 0
            str = ""
            tmp = ""

            for x in range(0, globals.images_per_char):
                str += char_list.pop()
                tmp += globals.dec_to_base((globals.base-1), globals.base)

            if (str == tmp):
                msg = False
                print()
                break
            else:
                print(chr(int(str, globals.base) + 32), end="")
