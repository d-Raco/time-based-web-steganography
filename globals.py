def init_globals():
    global images_per_char
    global base
    global inter_delay
    global maximum_ascii_char_num
    global non_important_characters
    global relevant_characters
    images_per_char = 2
    base = 10
    inter_delay = 4
    maximum_ascii_char_num = 126
    non_important_characters = 31
    relevant_characters = maximum_ascii_char_num - non_important_characters

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
