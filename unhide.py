import requests
from requests.exceptions import HTTPError
import globals
from time import time
from bs4 import BeautifulSoup

# Define global variables
globals.init_globals()

# URL of the webpage
webpage = 'http://localhost/Lab_Steganography/'

try:
    # Request the web-page
    r = requests.get(webpage)

    # If the response was successful, no Exception will be raised
    r.raise_for_status()
except HTTPError as http_err:
    print('HTTP Error: ' + str(http_err))
except Exception as err:
    print('Other Error: ' + str(err))
else:
    # Get the HTML of the web-page
    soup = BeautifulSoup(r.text, 'html.parser')

    # Initialize variables
    success = False
    retry = True
    char_list = []
    minimum_delay = ""

    # Claculate the minimum delay used to identify the separators between the message, the checksum and the rest of coverup additional images
    for x in range(0, globals.images_per_char):
        minimum_delay += '0'

    while retry:
        # Initialize variables
        retry = False
        msg = True
        check = False
        checksum = 0
        index = 0
        msg_delay = ""

        # Delete any elements present in the list
        while char_list:
            char_list.pop()

        # Iterate all <img> HTML elements
        for item in soup.find_all('img'):
            if retry:
                # Checksum did not match, begin all the process once again
                break
            else:
                if (msg or check):
                    # If it is part of the message or checksum, get the image
                    r = requests.get(webpage + item['src'])

                    # Calculate the delay of the image in the specified base
                    delay = globals.dec_to_base((r.elapsed.total_seconds() * 1000/globals.inter_delay), globals.base)

                    # Insert the delay into the list
                    char_list.insert(0, delay)
                    index += 1

                    # Enter when the delays of a single character of the message have been gathered
                    if (msg and (index % globals.images_per_char == 0)):
                        index = 0
                        msg_delay = ""

                        # Concatenate all the delays of the specific character of the message and calculate the checksum at the same time
                        for x in range(0, globals.images_per_char):
                            if len(char_list) > 0:
                                img_delay = char_list.pop()
                                msg_delay += img_delay
                                checksum += int(img_delay, globals.base)

                        # Check if it is the end of the message (the character is a separator; minimum delay)
                        if (msg_delay == minimum_delay):
                            # End of the message
                            msg = False

                            # Begin the checksum process
                            check = True
                            msg_delay = ""

                            # Translate the checksum from decimal into the specified base
                            checksum = globals.dec_to_base(checksum, globals.base)
                            print()
                        else:
                            print(chr(int(msg_delay, globals.base) + globals.non_important_characters), end="")

                    # Check if the sent checksum is the same as the one calculated
                    elif (check):
                        # Get the checksum
                        msg_delay += char_list.pop()

                        # Check if the length of the received checksum and the calculated checksum match and if a separator has been reached
                        if (len(msg_delay[:-globals.images_per_char]) == len(str(checksum)) and (msg_delay[-globals.images_per_char:] == minimum_delay)):
                            # Substract the separator
                            msg_delay = msg_delay[:-globals.images_per_char]

                            # Check if the calculated checksum and the received one are the same
                            if (checksum == msg_delay):
                                # Checksum matched
                                success = True
                                print('Checksum matched')
                                break
                            else:
                                # Checksum did not match, begin the whole process again
                                retry = True
                        elif (len(msg_delay[:-globals.images_per_char]) > len(str(checksum))):
                            # The checksum received is longer than the calculated checksum, something went wrong. Begin the whole process again
                            retry = True
        if not success:
            # Checksum did not match, begin the whole process again
            print('Error: Checksum did not match')
            retry = True
