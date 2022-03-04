def init_globals():
    ''' Initialize some global variables used both by the stego-web creation script and the script used to decode the stego-message'''

    # Number of images that encode a single character
    global images_per_char
    images_per_char = 3

    # Numerical based used per image-delay (number of possible symbols that the delay of a single image can encode)
    global base
    base = 5

    # Delay between symbols, in milliseconds
    global inter_delay
    inter_delay = 80

    # Maximum value of the alphabet that is going to be used (i.e., number of the ascii character with the highest decimal value from all the possible ascii characters that are going to be used in the message)
    global maximum_ascii_char_num
    maximum_ascii_char_num = 126

    # Number of ascii characters from the beggining of the ascii table that will not be used in the message (improves the performance). Consider that the character with the number 0 should not be used, as it is reserved for dividing the message and checksum.
    global non_important_characters
    non_important_characters = 31

    # Length of the alphabet used
    global relevant_characters
    relevant_characters = maximum_ascii_char_num - non_important_characters

def dec_to_base(num, base):
    ''' Transforms an integer number into any base smaller than or equal to 36'''
    base_num = ""
    while num > 0:
        dig = int(num % base)
        if dig < 10:
            base_num += str(dig)
        else:
            # Transform to the equivalent uppercase letter
            base_num += chr(ord('A')+dig-10)
        num //= base

    # Reverse the string
    base_num = base_num[::-1]
    return base_num
