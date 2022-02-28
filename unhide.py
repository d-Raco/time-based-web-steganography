import requests
from time import time
from bs4 import BeautifulSoup

base = 11

def dec_to_base(num, base):  #Maximum base - 36
    base_num = ""
    while num>0:
        dig = int(num%base)
        if dig<10:
            base_num += str(dig)
        else:
            base_num += chr(ord('A')+dig-10)  #Using uppercase letters
        num //= base

    base_num = base_num[::-1]  #To reverse the string
    return base_num

r = requests.get('http://localhost/Lab_Steganography/index.html')

soup = BeautifulSoup(r.text, 'html.parser')
msg = False
char1 = ''
char2 = ''

for item in soup.find_all('img'):
    if (item['id'] == '1'):
        msg = True
    elif (msg):
        r = requests.get('http://localhost/Lab_Steganography/' + item['src'])
        delay = dec_to_base((r.elapsed.total_seconds() * 1000/100), base)

        if (int(item['id']) % 2 == 0):
            char1 = delay
        else:
            char2 = delay

            if (char1 == 'A' and char2 == 'A'):
                msg = False
                print()
                break
            else:
                print(chr(int(char1 + char2, base) + 32), end="")
