import requests
from requests.exceptions import HTTPError
import globals
from time import time
from bs4 import BeautifulSoup

# Define global variables
globals.init_globals()

try:
    r = requests.get('http://localhost/Lab_Steganography/index.html')

    # If the response was successful, no Exception will be raised
    r.raise_for_status()
except HTTPError as http_err:
    print('HTTP Error: ' + str(http_err))
except Exception as err:
    print('Other Error: ' + str(err))
else:
    soup = BeautifulSoup(r.text, 'html.parser')

    retry = True
    char_list = []
    minimum_delay = ""

    for x in range(0, globals.images_per_char):
        minimum_delay += '0'

    while retry:
        retry = False
        msg = False
        check = False
        checksum = 0
        index = 0
        msg_delay = ""
        while char_list:
            char_list.pop()

        for item in soup.find_all('img'):
            if retry:
                break
            else:
                # Wait until the start of the message
                if (not msg and item['id'] == str(globals.images_per_char-1)):
                    msg = True

                elif (msg or check):
                    r = requests.get('http://localhost/Lab_Steganography/' + item['src'])
                    delay = globals.dec_to_base((r.elapsed.total_seconds() * 1000/globals.inter_delay), globals.base)

                    char_list.insert(0, delay)
                    index += 1

                    # Beginning of the message
                    if (msg and (index % globals.images_per_char == 0)):
                        index = 0
                        msg_delay = ""

                        for x in range(0, globals.images_per_char):
                            if len(char_list) > 0:
                                img_delay = char_list.pop()
                                msg_delay += img_delay
                                checksum += int(img_delay, globals.base)

                        if (msg_delay == minimum_delay):
                            msg = False
                            check = True
                            msg_delay = ""
                            checksum = globals.dec_to_base(checksum, globals.base)
                            print()
                        else:
                            print(chr(int(msg_delay, globals.base) + globals.non_important_characters), end="")

                    # Check if the sent checksum is the same as the one calculated
                    elif (check):
                        msg_delay += char_list.pop()

                        if (len(msg_delay[:-globals.images_per_char]) == len(str(checksum)) and (msg_delay[-globals.images_per_char:] == minimum_delay)):
                            check = False
                            msg_delay = msg_delay[:-globals.images_per_char]

                            if (checksum == msg_delay):
                                print('Checksum successful')
                                break
                            else:
                                retry = True
                                print('Checksum failed')
                        elif (len(msg_delay[:-globals.images_per_char]) > len(str(checksum))):
                            retry = True
                            print('Checksum failed')
